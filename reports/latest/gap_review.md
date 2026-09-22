# 근거 공백 검수

원래 공백을 삭제하지 않고 종합 시점의 판단과 근거를 보존합니다. 해소 여부의 의미 검수는 사람에게 남깁니다.

## gap-research_kivi-1 · research_kivi

**원래 공백:** Agentic AI가 기업 IT 사업 문서를 검토하는 실제 데이터와 에이전트 도구호출 환경에서 KIVI의 정확도·지연·동시성·운영 안정성은 unknown이다.

**종합 판단:** unresolved

**판단 이유:** KIVI의 비목표 모델·ShareGPT 합성 workload에서 wall-clock 효율과 조건부 정확도 실험 범위는 확인되지만, 기업 IT 문서의 실제 데이터와 Agent 도구호출 환경에서 정확도·지연·동시성·운영 안정성을 검증한 근거는 제공 자료에서 확인되지 않는다.

**근거 주장:** [research_kivi-2](citation_review.md#research_kivi-2), [research_kivi-3](citation_review.md#research_kivi-3), [research_kivi-4](citation_review.md#research_kivi-4), [domain-1](citation_review.md#domain-1)

**사람 검수:** 미검수

## gap-research_kivi-2 · research_kivi

**원래 공백:** Figure 5 발췌에서 절대 batch 크기, KIVI-2/KIVI-4 구분, latency·accuracy, 반복 횟수와 세부 소프트웨어 설정은 검색 미확인이다.

**종합 판단:** unresolved

**판단 이유:** Figure 5(p7–8, arXiv:2402.02750v2)의 Llama-2-7B·ShareGPT 합성 workload·residual 32/128·A100 80GB 및 peak memory·throughput·최대 batch 비교 범위는 확인된다. 그러나 절대 batch, KIVI-2/KIVI-4 매핑, latency·accuracy, 반복 횟수와 세부 software 설정은 검색 미확인으로 남는다.

**근거 주장:** [research_kivi-3](citation_review.md#research_kivi-3)

**사람 검수:** 미검수

## gap-research_kivi-3 · research_kivi

**원래 공백:** 제공된 코드 발췌에는 license 문구가 없으며, 이는 라이선스 부재가 아니라 검색 미확인이다. 독립 재현과 production 운용도 unknown이다.

**종합 판단:** unresolved

**판단 이유:** KIVI 논문 2402.02750v2와 공식 README snapshot version baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf는 식별되지만, 코드 발췌의 license 문구는 검색 미확인이지 부재가 아니다. 독립 재현과 production 운용도 확인되지 않아 공백이 남는다.

**근거 주장:** [research_kivi-4](citation_review.md#research_kivi-4), [stakeholder-3](citation_review.md#stakeholder-3), [market-3](citation_review.md#market-3)

**사람 검수:** 미검수

## gap-research_infinigen-1 · research_infinigen

**원래 공백:** 기업 IT 문서 검토 Agentic AI의 대표 사용조건에서 정확도·지연·동시성·SLO·지속운용을 검증한 공개 근거는 unknown이다.

**종합 판단:** unresolved

**판단 이유:** InfiniGen의 CPU KV pool·동적 prefetch 구조와 오프로딩 benchmark 범위는 확인된다. 다만 p11 Table 2의 80% KV-cache memory-limit 축출 정책·perplexity와 p12 Figure 17의 alpha·partial-weight ratio accuracy·latency sweep은 별도 실험이므로, 기업 IT 문서 Agentic AI의 정확도·지연·동시성·SLO·지속운용 검증으로 연결되지 않는다.

**근거 주장:** [research_infinigen-1](citation_review.md#research_infinigen-1), [research_infinigen-2](citation_review.md#research_infinigen-2), [research_infinigen-3](citation_review.md#research_infinigen-3), [research_infinigen-4](citation_review.md#research_infinigen-4)

**사람 검수:** 미검수

## gap-market-1 · market

**원래 공백:** 두 기술 모두 제공 자료에서 기업 IT 사업 문서를 검토하는 Agentic AI의 실제 데이터·도구호출 환경에서 정확도, 근거성·환각, latency, 동시성, SLO와 지속운용을 검증한 결과는 unknown이다.

**종합 판단:** unresolved

**판단 이유:** 공개 근거는 KIVI의 합성 workload 효율 실험과 InfiniGen의 오프로딩·축출·alpha 관련 실험 범위를 보여주지만, 실제 기업 IT 문서·Agent 도구호출 환경의 정확도·근거성·환각, latency, 동시성, SLO와 지속운용은 확인되지 않는다. 따라서 시장 관점 공백은 미해소다.

**근거 주장:** [research_kivi-3](citation_review.md#research_kivi-3), [research_infinigen-2](citation_review.md#research_infinigen-2), [research_infinigen-3](citation_review.md#research_infinigen-3), [market-1](citation_review.md#market-1), [domain-1](citation_review.md#domain-1), [domain-4](citation_review.md#domain-4), [domain-6](citation_review.md#domain-6)

**사람 검수:** 미검수

## gap-market-2 · market

**원래 공백:** 제공 자료에서 공개 기업 채택·고객 사례·도입률·시장 규모와 SK AX 내부 구조 또는 KIVI·InfiniGen 채택 사실은 확인되지 않는다. 이는 제공 발췌의 검색 미확인이며 원문 전체나 비공개 도입의 부재를 뜻하지 않는다.

**종합 판단:** unresolved

**판단 이유:** market-1·market-4와 domain-1·domain-4는 두 기술의 공개 논문·저장소를 기술·생태계 신호로만 다루며 공개 기업 채택·고객 사례·도입률, SK AX 내부 구조·채택 사실을 확인하지 않는다. 시장 규모와 원문 전체·비공개 도입 여부까지 해소한 근거는 없어 공백을 유지한다.

**근거 주장:** [market-1](citation_review.md#market-1), [market-4](citation_review.md#market-4), [domain-1](citation_review.md#domain-1), [domain-4](citation_review.md#domain-4)

**사람 검수:** 미검수

## gap-market-3 · market

**원래 공백:** CAPEX/OPEX, 클라우드·온프레미스 TCO, 통합·유지보수 인력, support 조건과 코드 저장소 license는 금액 또는 확정 조건으로 산정할 근거가 제공 발췌에서 unknown이다.

**종합 판단:** unresolved

**판단 이유:** market-3·market-6는 KIVI의 메모리 효율과 InfiniGen의 오프로딩 효율을 비용 후보로만 연결한다. KIVI 논문 2402.02750v2·README snapshot baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf와 InfiniGen 논문 2406.19707v1·README snapshot f6a08e32c16d3fdbe8839a95775f2b1e2a2690e36e6ee9d8ec683d6c24e89a90은 식별되지만 CAPEX/OPEX·TCO·통합·유지보수·지원·라이선스의 금액 또는 확정 조건은 확인되지 않는다. 라이선스 미확인은 부재가 아니므로 공백은 남는다.

**근거 주장:** [market-3](citation_review.md#market-3), [market-6](citation_review.md#market-6), [stakeholder-3](citation_review.md#stakeholder-3), [stakeholder-6](citation_review.md#stakeholder-6)

**사람 검수:** 미검수

## gap-market-4 · market

**원래 공백:** 동일 모델·정밀도·입출력 길이·batch·장비·baseline에서 두 기술을 직접 비교한 기업 문서 검토 benchmark와 독립 재현 결과가 unknown이다.

**종합 판단:** unresolved

**판단 이유:** research_kivi-3·research_infinigen-3는 서로 다른 모델·입출력 길이·batch·장비·baseline의 별도 실험이다. domain-3·domain-6는 동일 기업 문서 조건의 A/B와 독립 재현을 제안할 뿐 보고된 결과를 제공하지 않으므로, 동일조건 benchmark와 독립 재현 공백은 미해결이다.

**근거 주장:** [research_kivi-3](citation_review.md#research_kivi-3), [research_infinigen-3](citation_review.md#research_infinigen-3), [market-3](citation_review.md#market-3), [market-6](citation_review.md#market-6), [domain-3](citation_review.md#domain-3), [domain-6](citation_review.md#domain-6)

**사람 검수:** 미검수

## gap-stakeholder-1 · stakeholder

**원래 공백:** 제공된 검색 발췌 범위에서 두 기술이 기업 IT 사업 문서의 조항 추출 정확도·누락·환각·근거 추적·Agentic tool-call 정확도를 검증한 결과는 확인되지 않아 unknown이다.

**종합 판단:** unresolved

**판단 이유:** stakeholder-1·stakeholder-4와 domain-1·domain-4는 목표업무를 시나리오 또는 unknown으로 구분하고, domain-2·domain-3·domain-6는 사실성·근거·누락 등을 측정할 검증 설계만 제시한다. 기업 문서의 조항 추출 정확도·누락·환각·근거 추적과 Agentic tool-call 정확도의 실제 결과는 제공 자료에서 확인되지 않는다.

**근거 주장:** [stakeholder-1](citation_review.md#stakeholder-1), [stakeholder-4](citation_review.md#stakeholder-4), [domain-1](citation_review.md#domain-1), [domain-2](citation_review.md#domain-2), [domain-4](citation_review.md#domain-4), [domain-3](citation_review.md#domain-3), [domain-6](citation_review.md#domain-6)

**사람 검수:** 미검수

## gap-stakeholder-2 · stakeholder

**원래 공백:** 장문·반복·동시 요청에서 기업 문서의 latency·SLO·동시성·장애 복구·지속운용 결과는 두 기술 모두 unknown이다. KIVI는 A100 wall-clock 효율 자체는 확인됐지만 반복 횟수와 software 세부가 남아 있다.

**종합 판단:** unresolved

**판단 이유:** research_kivi-3·stakeholder-2가 확인하는 것은 Llama-2-7B·ShareGPT synthetic workload·단일 A100 80GB의 KIVI wall-clock 효율 anchor뿐이며, 반복 횟수·software 세부와 문서 SLO·동시성·장애 복구·지속 운용은 미확인이다. research_infinigen-3·stakeholder-5·research_infinigen-4의 별도 speedup·alpha 실험도 목표 업무의 latency/SLO 결과가 아니므로 공백은 유지된다.

**근거 주장:** [research_kivi-3](citation_review.md#research_kivi-3), [stakeholder-2](citation_review.md#stakeholder-2), [research_infinigen-3](citation_review.md#research_infinigen-3), [stakeholder-5](citation_review.md#stakeholder-5), [research_infinigen-4](citation_review.md#research_infinigen-4)

**사람 검수:** 미검수

## gap-stakeholder-3 · stakeholder

**원래 공백:** KIVI Figure 5의 KIVI-2/KIVI-4 variant별 정밀도, 절대 batch, latency·accuracy, 반복·software 설정과 기업 문서 독립 재현·production 검증은 검색 발췌에서 미확인이다.

**종합 판단:** unresolved

**판단 이유:** Figure 5의 모델·합성 workload·잔여 길이·A100·peak memory/throughput 조건은 확인됐지만, KIVI-2/KIVI-4 정밀도 매핑, 절대 batch, latency·accuracy, 반복·software 상세와 기업 문서 독립 재현·production 검증은 여전히 미확인이다.

**근거 주장:** [research_kivi-3](citation_review.md#research_kivi-3), [research_kivi-4](citation_review.md#research_kivi-4)

**사람 검수:** 미검수

## gap-stakeholder-4 · stakeholder

**원래 공백:** InfiniGen Table 2의 80% 축출 정책을 selective prefetch의 문서 정확도와 연결할 수 없으며, Figure 17의 모델·정밀도·길이·batch·장비·데이터셋·baseline·측정/시뮬레이션·반복 조건은 검색 발췌에서 미확인이다.

**종합 판단:** unresolved

**판단 이유:** Table 2의 80% FIFO/LRU/Counter 축출 perplexity와 Figure 17의 alpha·partial-weight ratio별 accuracy·latency는 확인됐지만, 전자는 selective prefetch의 문서 정확도 근거가 아니며 Figure 17의 세부 실험 조건도 미확인이다.

**근거 주장:** [research_infinigen-1](citation_review.md#research_infinigen-1), [research_infinigen-2](citation_review.md#research_infinigen-2)

**사람 검수:** 미검수

## gap-stakeholder-5 · stakeholder

**원래 공백:** 두 기술의 제공 발췌에서 저장소 license 문구와 CPU KV pool의 접근통제·보존정책·데이터 이동 통제·오류 책임경계·검수기준은 unknown이다. SK AX 내부 구조와 KIVI·InfiniGen의 실제 채택·도입 여부도 제공 근거에서 확인하지 않는다.

**종합 판단:** unresolved

**판단 이유:** 두 논문과 공식 저장소의 식별 및 CPU KV pool·prefetch 구조는 확인됐지만, license 문구, 접근통제·보존·데이터 이동 통제, 오류 책임·검수기준, SK AX 내부 구조와 실제 채택은 확인되지 않았다. 검색 미확인은 부재를 뜻하지 않는다.

**근거 주장:** [stakeholder-3](citation_review.md#stakeholder-3), [stakeholder-6](citation_review.md#stakeholder-6), [market-1](citation_review.md#market-1), [market-4](citation_review.md#market-4)

**사람 검수:** 미검수

## gap-domain-1 · domain

**원래 공백:** 제공된 AiPMO 설명과 논문 benchmark 사이에서 실제 RFP·계약·사업계획서·발주 문서와 Agent 도구 chain을 사용한 사실성·근거 인용·리스크 recall, latency, peak 또는 CPU/GPU memory, 동시성 SLO, 접근통제·보안 격리 및 생산 운용 안정성은 양 기술 모두 unknown이다.

**종합 판단:** unresolved

**판단 이유:** AiPMO 설명과 각 논문의 실험 anchor 및 제안된 A/B 검증 설계는 확인됐지만, 실제 RFP·계약 등 기업 문서와 Agent 도구 chain에서의 사실성·근거 인용·리스크 recall, 지연·메모리·동시성 SLO·보안 격리·생산 안정성 결과는 양 기술 모두 미확인이다.

**근거 주장:** [domain-1](citation_review.md#domain-1), [domain-3](citation_review.md#domain-3), [domain-4](citation_review.md#domain-4), [domain-6](citation_review.md#domain-6)

**사람 검수:** 미검수

## gap-domain-2 · domain

**원래 공백:** KIVI Figure 5 발췌에서 절대 batch, KIVI-2/KIVI-4 정밀도 매핑, latency·accuracy, 반복 횟수·software detail 및 명시적 simulation 여부가 미확인이다. 제공된 KIVI 코드 발췌의 license 문구도 검색 미확인이며 라이선스 부재를 뜻하지 않는다.

**종합 판단:** unresolved

**판단 이유:** KIVI Figure 5의 wall-clock 비교 조건과 전체적인 효율 결과 범위는 확인됐지만, 절대 batch, KIVI-2/KIVI-4 정밀도 매핑, latency·accuracy, 반복·software 상세와 명시적 simulation 여부는 미확인이다. 코드 license 미확인은 라이선스 부재가 아니다.

**근거 주장:** [research_kivi-3](citation_review.md#research_kivi-3), [research_kivi-4](citation_review.md#research_kivi-4)

**사람 검수:** 미검수

## gap-domain-3 · domain

**원래 공백:** InfiniGen Figure 17의 모델·정밀도·입출력 길이·batch·장비·dataset·baseline·측정/시뮬레이션 세부와 기업 문서 재현은 제공 발췌에서 미확인이다. Table 2의 80% 축출 정책 결과는 이 공백을 selective prefetch 검증으로 대체하지 않는다.

**종합 판단:** resolved

**판단 이유:** research_infinigen-2가 Figure 17의 모델·정밀도·입출력 길이·batch·장비·dataset·baseline·측정/시뮬레이션 세부와 기업 문서 재현이 제공 발췌에서 미확인임을 명시했다. 또한 Table 2의 80% FIFO·LRU·Counter 축출 결과는 selective prefetch와 별도 실험이므로 해당 공백을 대체하지 않는다는 구분도 확인된다.

**근거 주장:** [research_infinigen-2](citation_review.md#research_infinigen-2)

**사람 검수:** 미검수
