from pathlib import Path
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request

from rag.budget import Budget, write_json
from rag.request_budget import PROTOCOL_MARGIN, InputBudgetExceeded, enforce_input_budget


class APIError(RuntimeError):
    pass


class Gateway:
    def __init__(self, settings, run_id, output_dir, cache_dir=None):
        settings.validate_paid()
        self.settings, self.run_id = settings, run_id
        self.output_dir = Path(output_dir)
        self.budget = Budget(settings)
        self.cached = {}
        self.input_counts = {}
        self.input_reserves = {}
        for path in sorted(Path(cache_dir).glob("calls/*.json")) if cache_dir else []:
            receipt = json.loads(path.read_text())
            if receipt.get("status") == "completed" and receipt.get("text_sha256") == hashlib.sha256(receipt["text"].encode()).hexdigest():
                self.cached[receipt["request_hash"]] = receipt

    def request(self, path, payload=None):
        raw = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
        req = urllib.request.Request("https://api.openai.com/v1/" + path, data=raw,
            headers={"Authorization": "Bearer " + self.settings.get("OPENAI_API_KEY"),
                     "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.settings.integer("OPENAI_TIMEOUT_SECONDS", 60)) as response:
            return json.load(response)

    def lookup(self):
        try:
            response = self.request("models/" + urllib.parse.quote(self.settings.get("OPENAI_MODEL"), safe=""))
            return {"status": "ok", "model_id": response["id"]}
        except urllib.error.HTTPError as exc:
            raise APIError(f"Model lookup HTTP {exc.code}; credential and response body hidden") from None

    def build_payload(self, purpose, instructions, content, schema=None, max_output=None):
        limit_out = max_output or self.settings.integer("LLM_MAX_OUTPUT_TOKENS", 8000)
        if limit_out > self.settings.integer("LLM_MAX_OUTPUT_TOKENS", 8000):
            raise ValueError("Requested output exceeds configured cap")
        payload = {"model": self.settings.get("OPENAI_MODEL"),
                   "reasoning": {"effort": self.settings.get("OPENAI_REASONING_EFFORT", "max")},
                   "service_tier": "default", "store": False, "instructions": instructions,
                   "input": content, "max_output_tokens": limit_out}
        if schema:
            payload["text"] = {"format": {"type": "json_schema", "name": purpose.replace("-", "_"),
                                           "strict": True, "schema": schema}}
        return payload

    @staticmethod
    def payload_hash(payload):
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def preflight(self, purpose, instructions, content, schema=None, max_output=None, reserve_input=0):
        """Exact count for every new request, before reservation or generation.

        Already-completed exact requests bypass counting and headroom, preserving
        successful response reuse. Token-count cache is keyed by the entire exact
        payload; planning and execution therefore do not count identical input twice.
        """
        payload = self.build_payload(purpose, instructions, content, schema, max_output)
        request_hash = self.payload_hash(payload)
        if request_hash in self.cached:
            return {'cached': True, 'request_hash': request_hash}
        limit_in = self.settings.integer("LLM_MAX_INPUT_TOKENS", 24000)
        if len(json.dumps(payload, ensure_ascii=False).encode()) + PROTOCOL_MARGIN > 200000:
            failure = InputBudgetExceeded(purpose, None, limit_in, reserve_input, 'short_context_byte_bound')
            write_json(self.output_dir / 'input_budget' / f'{purpose}-{request_hash}.json', failure.diagnostic)
            raise failure
        if request_hash not in self.input_counts:
            count_payload = {k: v for k, v in payload.items() if k in {"model", "reasoning", "input", "instructions", "text"}}
            try:
                response = self.request("responses/input_tokens", count_payload)
            except (urllib.error.URLError, TimeoutError):
                raise APIError("Input token counting failed; no generation request sent") from None
            count = response.get('input_tokens')
            if type(count) is not int or count < 0:
                raise APIError('Invalid exact input token count; no generation request sent')
            self.input_counts[request_hash] = count
        count = self.input_counts[request_hash]
        try:
            enforce_input_budget(purpose, count, limit_in, reserve_input)
        except InputBudgetExceeded as failure:
            write_json(self.output_dir / 'input_budget' / f'{purpose}-{request_hash}.json', failure.diagnostic)
            raise
        self.input_reserves[request_hash] = max(reserve_input, self.input_reserves.get(request_hash, 0))
        verified_reserve = self.input_reserves[request_hash]
        diagnostic = {'status': 'passed', 'purpose': purpose, 'cached': False,
                      'request_hash': request_hash, 'input_tokens': count, 'input_limit': limit_in,
                      'protocol_margin': PROTOCOL_MARGIN, 'repair_reserve': verified_reserve,
                      'available_input_tokens': limit_in - PROTOCOL_MARGIN - verified_reserve,
                      'generation_sent': False}
        write_json(self.output_dir / 'input_budget' / f'{purpose}-{request_hash}.json', diagnostic)
        return diagnostic

    def generate(self, purpose, instructions, content, schema=None, max_output=None):
        limit_in = self.settings.integer("LLM_MAX_INPUT_TOKENS", 24000)
        payload = self.build_payload(purpose, instructions, content, schema, max_output)
        limit_out = payload['max_output_tokens']
        request_hash = self.payload_hash(payload)
        if request_hash in self.cached:
            receipt = {**self.cached[request_hash], "reused_in_run": self.run_id}
            write_json(self.output_dir / "calls" / f"{purpose}-reused.json", receipt)
            return receipt["text"]
        self.preflight(purpose, instructions, content, schema, max_output)
        for attempt in range(int(self.settings.get("OPENAI_MAX_RETRIES", "2")) + 1):
            reservation = self.budget.reserve(self.run_id, purpose, limit_in, limit_out)
            try:
                response = self.request("responses", payload)
            except (urllib.error.URLError, TimeoutError) as exc:
                status = exc.code if isinstance(exc, urllib.error.HTTPError) else None
                retryable = status is None or status == 429 or status >= 500
                if retryable and attempt < int(self.settings.get("OPENAI_MAX_RETRIES", "2")):
                    time.sleep(2 ** attempt)
                    continue
                raise APIError(f"{purpose}: HTTP {status or 'network/timeout'}; reservation retained") from None
            self.budget.settle(reservation, response)
            text = "".join(part.get("text", "") for item in response.get("output", [])
                           if item.get("type") == "message" for part in item.get("content", [])
                           if part.get("type") == "output_text")
            receipt = {"purpose": purpose, "request_hash": request_hash, "status": response.get("status"),
                       "model": response.get("model"), "usage": response.get("usage"),
                       "service_tier": response.get("service_tier"), "text": text,
                       "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                       "incomplete_details": response.get("incomplete_details")}
            write_json(self.output_dir / "calls" / f"{purpose}-{reservation}.json", receipt)
            if response.get("status") != "completed":
                raise APIError(f"{purpose}: generation incomplete; inspect receipt, do not silently raise output cap")
            return text
        raise AssertionError("unreachable")
