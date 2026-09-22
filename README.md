# KV Cache 다관점 평가 에이전트

KIVI와 InfiniGen을 기업 IT 사업 문서 검토라는 공통 시나리오에서 비교합니다. 논문과 공식 자료를 검색해 기술 성숙도·시장성·이해관계자·도메인 적용을 분석하고, 근거를 추적할 수 있는 Markdown 보고서를 생성합니다.

이 저장소는 팀의 **진행 상황 공유용 스냅샷**입니다. 팀원별 제출 Git 이력과 별개로 운영합니다. 현재 보완 작업은 진행 중이며, 아래 보고서는 가장 최근에 생성·자동 검증을 마친 결과입니다.

- [설계 정본](docs/design-report.md)
- [현재 진행 상태](PROGRESS.md)
- [생성된 보고서](reports/latest/report.md) · [인용 검수표](reports/latest/citation_review.md) · [공백 검수표](reports/latest/gap_review.md)
- [검색 실험](docs/retrieval-experiments.md) · [초기 임베딩 비교](docs/embedding-benchmark.md)

## 실행

Python 3.11~3.13과 uv를 사용합니다.

```bash
uv sync --frozen
cp -n .env.example .env.local
uv run python -m pytest -q
uv run python app.py --prepare
# .env.local의 OPENAI_API_KEY와 USD_TO_KRW를 설정한 후 유료 생성
uv run python app.py --config config/run.yaml
```

`--prepare`는 공개 자료와 로컬 임베딩을 준비합니다. 보고서 생성은 OpenAI API를 사용합니다. API 키·개인 환경파일·누적 사용량 장부는 저장소에 포함하지 않습니다. 유료 실행 담당자는 하나의 누적 장부를 유지해야 하며, 다른 환경의 사용량은 자동 합산되지 않습니다.

기본 모델은 `gpt-5.6-luna`, 추론 `max`입니다. 입력 한도 24,000과 출력 한도 64,000을 유지하며, 입력 크기를 생성 전에 확인합니다. 수정 요청은 오류가 있는 부분으로 제한하고 기존 근거를 보존합니다. 가격과 비용 계산은 [운영 비용](docs/pricing.md)에 설명했습니다.

## 구조

| 경로 | 역할 |
| --- | --- |
| `app.py`, `rag/graph.py` | 실행·관점별 평가·병렬 처리와 합류 |
| `rag/corpus.py`, `rag/source_discovery.py` | 논문 처리·임베딩·검색·공식 자료 수집 |
| `rag/llm.py`, `rag/budget.py`, `rag/request_budget.py`, `rag/repair.py` | 모델 호출·비용·입력 한도·부분 수정 |
| `rag/schemas.py`, `rag/evidence.py`, `rag/render.py` | 구조화 결과·근거 검증·보고서 작성 |
| `config/`, `eval/`, `tests/` | 실행 설정·검색 질문·회귀 검사 |
| `experiments/` | 기존 검색 실험의 원시 결과 |

기술 조사에는 논문 벡터 검색을, 후속 세 관점에는 공식 웹 사본의 어휘 검색을 사용합니다. 후속 관점은 공통 기술 근거도 함께 전달받습니다. 공개 사례를 적용 시나리오로 삼으며 실제 사내 기밀문서는 사용하지 않습니다.

## Contribution

| 팀원 | 수행 역할 |
| --- | --- |
| 김기현 | README 재현·PDF 형식·발표 정리 |
| 김도현 | PDF 자료 처리·임베딩·검색·출처 도구 |
| 박병준 | 그래프·State·모델 호출·최종 통합 |
| 홍수정 | 원문·질문셋·관점별 주장·조건 검수 |

코드와 문서 작성에 Codex를 활용했습니다. 팀은 담당 영역을 검토하고 실행 결과를 확인합니다. 자동 검증 성공 상태인 `human_review_pending`은 인용 의미와 최종 보고서의 사람 검수가 남았다는 뜻입니다.
