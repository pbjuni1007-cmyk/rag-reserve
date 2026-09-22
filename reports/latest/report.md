# SUMMARY

[팀 추론] 공개 근거의 목표 도메인 잠정 TRL은 3–4로 평가한다. CUDA/Triton 구현과 여러 모델·LongBench·ShareGPT형 실험은 실험실 검증을 보이지만, 기업 IT 문서 검토의 정확도·지연·동시성 및 운영 검증은 제공 근거에서 확인되지 않아 TRL 5로 올릴 근거는 없다. [4, 물리 p.6] [4, 물리 p.2] [4, 물리 p.9] [4, 물리 p.1]

[팀 추론] 공개 정보상 목표 업무 기준 잠정 TRL은 3–4(기술 자체의 실험실 검증 상한 4)다. OPT·Llama-2 평가와 오프로딩 구현은 확인되지만, 기업 IT 문서 검토 Agentic AI의 대표 사용조건·SLO·지속운용은 검증되지 않았다. [2, 물리 p.2] [2, 물리 p.9]

[팀 추론] KIVI의 A100·Llama-2-7B·ShareGPT wall-clock과 InfiniGen의 A6000·OPT·FlexGen 대비 speedup은 조건이 달라 기업 문서업무의 공통 우열이나 직접 순위를 제시하지 않는다. [4, 물리 p.8] [4, 물리 p.7] [4, 물리 p.2] [2, 물리 p.12] [2, 물리 p.9]

**대상 기술:** KIVI / InfiniGen  
**단일 도메인:** 기업의 IT 사업 문서 검토를 지원하는 Agentic AI

> 검토본. PDF 변환 후 SUMMARY 반 페이지·페이지 배치는 사용자가 확인합니다.

**적용 가정:** 공개 AiPMO 사례를 참고한 RFP·계약·사업 문서 검토. 장문과 반복 요청은 팀의 적용 가정이며 SK AX 내부 구조·기술 도입 사실이 아님.

# 기술 성숙도

## KIVI · research_kivi-1

**출처 사실 · research_kivi-1**

KIVI는 조정 없이 동작하는 비대칭 2-bit KV 캐시 양자화로, 키는 채널별·값은 토큰별로 처리하고 완성 그룹만 압축한다. 그룹을 못 이룬 잔여 캐시는 full precision으로 보존해 어텐션에서 결합한다. [4, 물리 p.2]

**조건:** 논문 p2의 방법 설명에 근거한다. 키는 per-channel, 값은 per-token이며 grouped/residual 분할을 사용한다. 구체적인 group size와 residual length는 실험별로 달라지고, Agentic AI의 기업 IT 문서·도구호출 조건은 미확인이다.

**한계:** 잔여 키·값 캐시는 full precision으로 남으므로 전체 KV 캐시가 모두 2-bit가 되는 방식은 아니다. GPU 구현에는 CUDA와 Triton이 사용되지만, 기업 IT 문서 검토에서의 정확도·지연은 제공 근거에서 확인되지 않는다.

## KIVI · research_kivi-2

**저자 보고 결과 · research_kivi-2**

저비트 설정은 모델·캐시 구조와 그룹·잔여 길이에 민감하다. Falcon의 multi-query attention에서 논문은 정확도 유지를 위해 4-bit가 필요하고 2-bit는 큰 정확도 하락 가능성이 있다고 보고했으며, group size 128은 성능을 낮추고 잔여 길이 효과도 일정하지 않았다. [4, 물리 p.6] [4, 물리 p.7]

**조건:** Table 3의 관련 조건은 Falcon의 multi-query attention과 16-bit·4-bit·2-bit 비교이며, 표에 제시된 작업 지표는 CoQA·TruthfulQA·GSM8K이다. Table 5의 그룹·잔여 길이 ablation은 Llama2-13B의 GSM8K에서 group size 32·64·128 및 residual length 32·64·96·128을 비교한다. 해당 발췌에서 장비·배치·입출력 길이·반복 횟수·소프트웨어 설정은 미확인이다.

**한계:** 이는 논문 실험에서 관찰된 조건부 제약이지 모든 모델이나 기업 문서 검토 업무의 보편적 결과가 아니다. Falcon의 4-bit·2-bit 관찰과 Table 5의 group/residual ablation은 서로 다른 실험 조건이며 목표 도메인 일반화는 미확인이다.

## KIVI · research_kivi-3

**저자 보고 결과 · research_kivi-3**

Figure 5의 wall-clock 실험은 ShareGPT 기반 합성 workload(평균 입력 161·출력 338토큰)에서 Llama-2-7B의 KIVI(R32/R128)와 FP16을 단일 A100 80GB로 비교해, 유사 peak memory에서 batch 최대 4배·throughput 2.35–3.47배를 보고했다. [4, 물리 p.7] [4, 물리 p.8]

**조건:** 모델은 Llama-2-7B, baseline은 FP16, KIVI residual length는 32와 128이다. 입력·출력 길이는 각각 평균 161·338토큰이며, ShareGPT 기반 synthetic workload를 사용했다. batch는 out-of-memory까지 증가시켰고 비교 기준은 유사한 maximum memory usage이다. 지표는 wall-clock 기반 peak memory·throughput·최대 batch size이며, 단일 NVIDIA A100 80GB에서 측정된 결과로 기술된다. 정밀도는 논문 전체에서 KIVI가 2-bit 방식으로 제시되지만 Figure 5의 variant별 정밀도 구분은 미확인이다.

**한계:** 조건은 arXiv 2402.02750v2의 p7–8 Figure 5 실험이다. workload는 실제 기업 문서가 아니라 ShareGPT 기반 합성 입력이다. Figure 5 발췌에서는 KIVI-2와 KIVI-4의 구분, 절대 batch 크기, latency·accuracy 수치, 반복 횟수와 세부 소프트웨어 설정이 검색 미확인이다.

## KIVI · research_kivi-4

**팀 추론 · research_kivi-4**

공개 근거의 목표 도메인 잠정 TRL은 3–4로 평가한다. CUDA/Triton 구현과 여러 모델·LongBench·ShareGPT형 실험은 실험실 검증을 보이지만, 기업 IT 문서 검토의 정확도·지연·동시성 및 운영 검증은 제공 근거에서 확인되지 않아 TRL 5로 올릴 근거는 없다. [4, 물리 p.6] [4, 물리 p.2] [4, 물리 p.9] [4, 물리 p.1]

**조건:** 근거가 확인된 환경은 Llama/Llama-2·Falcon·Mistral 모델, LongBench와 생성 과제, CUDA/Triton GPU 구현, ShareGPT 기반 합성 wall-clock workload이다. 이는 실험실 수준의 공개 검증으로 해석했으며, 기업 IT 사업 문서의 장문·반복·동시 요청과 Agentic 도구 연계는 대표 사용조건 검증으로 포함하지 않았다.

**한계:** TRL은 논문이 인증한 값이 아니라 공개 논문·코드와 실험 범위를 바탕으로 한 팀 추론이다. source_metadata상 논문은 2402.02750v2(2024, SHA-256 df31ef32d71bfb280c533c5db8220cadf5ef42076bf45d82ba4c8da8e50ea5f4), 공식 README snapshot은 version baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf, date unknown이다. 제공 발췌에는 코드 license 문구가 없어 license는 검색 미확인이지 부재가 아니다. 독립 재현·생산 운용·기업 IT 문서 검토 실증도 미확인이다.

## InfiniGen · research_infinigen-1

**출처 사실 · research_infinigen-1**

InfiniGen은 이전 층의 attention 입력과 다음 층의 부분 query weight·key cache로 다음 attention을 추정해, 필요한 KV만 CPU 풀에서 GPU로 동적 prefetch하고 KV cache pool은 CPU에 유지한다. [2, 물리 p.2] [2, 물리 p.1]

**조건:** 설계 조건은 오프로딩 기반 추론이다. Prefill에서 partial weights를 만들고, decoding의 Layer i−1에서 Layer i attention을 추정한 뒤 CPU KV pool에서 필요한 항목을 GPU로 가져온다. 이는 논문 구조 설명이며 기업 문서 검토 workload의 실험 조건은 제공 자료에서 확인되지 않는다.

**한계:** 선택적 prefetch가 full-cache와 수학적으로 동일하거나 무손실이라는 보장은 제공 발췌에서 확인되지 않는다. 기업 IT 문서 검토를 지원하는 Agentic AI에서의 적합성도 unknown이다.

## InfiniGen · research_infinigen-2

**팀 추론 · research_infinigen-2**

선택적 가져오기를 full-cache와 동일한 무손실 동작으로 단정할 수 없다. 80% KV 축출 비교의 OPT-13B FIFO perplexity는 WikiText-2 30.99·PTB 33.84였고, alpha와 부분 가중치 비율은 정확도·지연·메모리 절충을 만든다. [2, 물리 p.11] [2, 물리 p.12] [2, 물리 p.13]

**조건:** 문서 기준은 arXiv:2406.19707v1의 Table 2(p11), Figure 17(p12), 부분 가중치 설명(p13)이다. Table 2는 sequence length 2048의 WikiText-2·PTB perplexity(lower is better)를 다루며, OPT-13B는 100%=10.55/12.78, 80-FIFO%=30.99/33.84, 80-LRU%=10.55/12.78, 80-Counter%=10.55/12.78(Wiki/PTB 순)이다. 표의 모델은 OPT-6.7B·13B·30B와 Llama-2-7B·13B이며 정밀도, 입력·출력 분리 길이, batch, 장비, 측정/시뮬레이션 여부는 발췌에서 미확인이다. Figure 17은 alpha·partial weight ratio별 accuracy와 inference latency 실험이며, 부분비율 sweep의 alpha=4와 선택 ratio=0.3이 보고되지만 해당 sweep의 모델·정밀도·길이·batch·장비·데이터셋·baseline·측정/시뮬레이션 여부는 미확인이다.

**한계:** Table 2의 80-FIFO/LRU/Counter는 KV cache memory limit에서의 축출 정책 비교이지 InfiniGen의 selective prefetch와 동일한 실험이 아니다. 따라서 FIFO perplexity를 InfiniGen selective prefetch의 정확도 손실로 직접 귀속하지 않는다. Figure 17은 별도의 alpha·partial-weight sweep이며 기업 문서업무에서의 재현은 unknown이다.

## InfiniGen · research_infinigen-3

**출처 사실 · research_infinigen-3**

확인된 속도 비교는 OPT 6.7B·13B·30B에서 입력 1,920·출력 128·배치 4로 수행되었고, RTX A6000–Xeon Gold 6136·PCIe 3.0×16에서 INT4·H2O·InfiniGen의 FlexGen 대비 speedup을 비교했다. [2, 물리 p.12] [2, 물리 p.9]

**조건:** 문서 기준은 arXiv:2406.19707v1, Section 5.1 및 Figure 16(b)이다. 확인된 모델은 OPT 6.7B·13B·30B, 입력 1,920 tokens, 출력 128 tokens, batch 4이다. 장비는 NVIDIA RTX A6000 48GB, Intel Xeon Gold 6136, DDR4-2666 96GB, CPU-GPU PCIe 3.0×16이다. 지표는 FlexGen 대비 speedup이고 비교 대상은 INT4·H2O·InfiniGen이다. InfiniGen 정밀도, Figure 16 speedup 데이터셋, 정확한 측정/시뮬레이션 여부는 제공 발췌에서 미확인이다.

**한계:** 이는 논문 오프로딩 benchmark의 setup이며 기업 IT 문서 검토의 정확도·지연·SLO를 확인한 결과가 아니다. INT4는 비교법의 정밀도 명칭일 뿐 InfiniGen의 정밀도는 확인되지 않는다.

## InfiniGen · research_infinigen-4

**팀 추론 · research_infinigen-4**

공개 정보상 목표 업무 기준 잠정 TRL은 3–4(기술 자체의 실험실 검증 상한 4)다. OPT·Llama-2 평가와 오프로딩 구현은 확인되지만, 기업 IT 문서 검토 Agentic AI의 대표 사용조건·SLO·지속운용은 검증되지 않았다. [2, 물리 p.2] [2, 물리 p.9]

**조건:** 근거 문서는 arXiv:2406.19707v1이다. 평가 범위는 modern offloading-based inference system, OPT 6.7B·13B·30B와 Llama-2 7B·13B, COPA·OpenBookQA·WinoGrande·PIQA·RTE few-shot task, WikiText-2·PTB 언어모델링 데이터셋이다. 일반 실험 장비로 NVIDIA RTX A6000 48GB, Intel Xeon Gold 6136, DDR4-2666 96GB, PCIe 3.0×16이 확인된다. InfiniGen official repository README의 source_metadata version은 f6a08e32c16d3fdbe8839a95775f2b1e2a2690e36e6ee9d8ec683d6c24e89a90이며 date는 unknown이다. 기업 문서 유형·대표 사용조건·운용 SLO·동시 요청·지속 운용은 제공 자료에서 확인되지 않는다.

**한계:** TRL은 팀의 공개근거 기반 잠정 판단이며 논문이 직접 인증한 값이 아니다. 논문 구현과 benchmark는 실험실 검증의 근거일 뿐 대표 사용조건 검증의 근거는 아니므로 4에서 5로 올리지 않았다. 공개 코드 자체도 TRL을 높이는 충분조건이 아니며, 독립 재현·배포 검증·저장소 라이선스는 제공 자료에서 확인되지 않는다.

# 시장성

| 비교 질문 | KIVI | InfiniGen |
| --- | --- | --- |
| 채택 동기·공개 신호 | **팀 추론 · market-1**<br><br>공개 코드와 ICML 논문은 KIVI를 Llama·Mistral·Falcon 및 LongBench 등에서 평가한 생태계 신호를 제공하지만, 기업 IT 문서 검토 Agentic AI의 공개 채택·고객 사례·도입률은 제공 자료에서 확인되지 않는다. [4, 물리 p.1] [4, 물리 p.2] [4, 물리 p.9]<br><br>**조건:** 논문 source_metadata는 arXiv:2402.02750v2(2024, SHA-256 df31ef32d71bfb280c533c5db8220cadf5ef42076bf45d82ba4c8da8e50ea5f4), 공식 README snapshot은 version baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf(date unknown)이다. 확인된 범위는 Llama/Llama-2·Falcon·Mistral, 생성 과제와 LongBench이며, RFP·계약·사업 문서와 Agentic 도구호출의 채택·운영 검증은 아니다. 장문·반복·동시 요청은 팀 분석 가정이고 SK AX 내부 구조·KIVI 채택 사실이 아니다.<br><br>**한계:** 코드 공개와 논문 평가·LongBench 결과는 기술·생태계 신호이지 기업 채택 증거가 아니다. 검색 발췌에서 채택이 확인되지 않았다는 뜻이며 논문 전체에 사례가 없거나 비공개 도입이 없다고 단정하지 않는다. 제공 발췌에는 코드 license 문구가 없어 라이선스는 검색 미확인이지 부재가 아니다. 기업 문서 검토의 정확도·지연·동시성·운영 SLO도 미확인이다. | **팀 추론 · market-4**<br><br>공개 논문 구현·공식 저장소와 OPT·Llama-2의 few-shot·언어모델링 평가는 생태계 신호지만, 기업 IT 문서 검토 Agentic AI의 공개 채택·고객 사례·도입률은 제공 자료에서 확인되지 않는다. [2, 물리 p.2] [2, 물리 p.9] [3, snapshot block 8, character 0]<br><br>**조건:** 논문 source_metadata는 arXiv:2406.19707v1(2024, SHA-256 267d689a1ded953f076eb93976c0ebeac1ad02029f1f7c9dd1c947aa05d7cb5f), 공식 README snapshot은 version f6a08e32c16d3fdbe8839a95775f2b1e2a2690e36e6ee9d8ec683d6c24e89a90(date unknown)이다. 평가 범위는 modern offloading-based inference system, OPT 6.7B·13B·30B, Llama-2 7B·13B, COPA·OpenBookQA·WinoGrande·PIQA·RTE와 WikiText-2·PTB 중심이다. 기업 RFP·계약·사업 문서, Agentic 도구호출, 장문·반복·동시 요청의 채택·운영 검증은 아니다.<br><br>**한계:** 논문 구현과 benchmark는 기술 성숙·생태계 신호이지 고객 채택의 증거가 아니다. 제공 발췌에서 채택 사례가 확인되지 않았다는 뜻이며 논문 전체에 사례가 없거나 비공개 도입이 없다고 단정하지 않는다. 저장소 license, 독립 재현, production 배포와 운영 SLO도 제공 자료에서 확인되지 않는다. |
| 대안·연동 | **적용 가정 · market-2**<br><br>GPU KV 메모리 절감과 플러그앤플레이를 우선하면 KIVI를 후보로 두고, CPU KV 풀·선택적 prefetch가 필요한 InfiniGen과 정확도 기준선 FP16을 동일 문서업무로 비교하는 선택 구조가 타당하다. [4, 물리 p.2] [2, 물리 p.1] [2, 물리 p.2] [4, 물리 p.8] [4, 물리 p.6] [4, 물리 p.7]<br><br>**조건:** KIVI Figure 5(p7–8, arXiv:2402.02750v2)는 ShareGPT 기반 synthetic workload(평균 입력 161·출력 338토큰), Llama-2-7B, residual length 32·128의 KIVI와 FP16을 단일 NVIDIA A100 80GB에서 비교했다. batch를 OOM까지 늘려 wall-clock peak memory·throughput을 비교했고, 유사 maximum memory에서 최대 4배 batch와 2.35×∼3.47× throughput을 보고했다. Figure 5의 KIVI-2/KIVI-4 정밀도 구분, 절대 batch, latency·accuracy, 반복 횟수·세부 software 설정은 검색 미확인이다. InfiniGen Figure 16(b)는 별도 조건으로 OPT 6.7B·13B·30B, 입력 1,920·출력 128토큰, batch 4, RTX A6000 48GB·Xeon Gold 6136·DDR4-2666 96GB·PCIe 3.0×16에서 FlexGen 대비 speedup을 비교했다. InfiniGen 정밀도·데이터셋·정확한 측정/시뮬레이션 여부는 미확인이다.<br><br>**한계:** 이는 공개 사례에서 추론한 적용 시나리오이며 목표 업무의 구매 우위나 두 논문의 성능 순위가 아니다. KIVI는 grouped cache만 양자화하고 residual key/value는 full precision으로 남긴다. Falcon의 multi-query 조건에서 4-bit 필요와 2-bit 정확도 저하 가능성이 보고됐지만 일반화는 unknown이다. InfiniGen의 선택적 prefetch도 full-cache와 수학적으로 동일하거나 무손실이라고 단정하지 않는다. | **적용 가정 · market-5**<br><br>CPU 메모리와 PCIe 계층을 활용해 장문 KV 전송을 줄이는 조건이면 InfiniGen을 검토하되, KIVI·FP16과 비교해야 하며 80% FIFO/LRU/Counter 축출 결과나 alpha 실험을 문서업무 우위로 직접 해석해서는 안 된다. [2, 물리 p.1] [2, 물리 p.2] [2, 물리 p.11] [2, 물리 p.12] [2, 물리 p.13] [4, 물리 p.2]<br><br>**조건:** Table 2(p11, arXiv:2406.19707v1)는 sequence length 2048의 WikiText-2·PTB perplexity(lower is better)를 OPT-6.7B·13B·30B와 Llama-2-7B·13B의 100% 및 80-FIFO/LRU/Counter pool에서 비교한다. OPT-13B의 Wiki/PTB는 100% 10.55/12.78, 80-FIFO 30.99/33.84, 80-LRU 10.55/12.78, 80-Counter 10.55/12.78이다. 정밀도, 입력·출력 분리 길이, batch, 장비, 측정/시뮬레이션 여부는 발췌에서 미확인이다. Figure 17(p12)은 alpha와 partial-weight ratio별 accuracy·inference latency를 보이며, p13은 alpha=4와 ratio=0.3 선택을 설명한다. 해당 sweep의 모델·정밀도·길이·batch·장비·데이터셋·baseline·측정/시뮬레이션 여부는 미확인이다.<br><br>**한계:** Table 2의 80% FIFO/LRU/Counter는 KV cache memory limit에서의 축출 정책 비교이지 InfiniGen의 selective prefetch 결과가 아니다. 따라서 FIFO perplexity를 InfiniGen의 정확도 손실로 직접 귀속하지 않는다. Figure 17의 alpha·partial-weight sweep도 별도 실험이며, 선택적 가져오기가 full-cache와 무손실로 동일하다는 결론이나 기업 문서업무 우위로 일반화할 수 없다. |
| 비용·유지 부담 | **미확인 · market-3**<br><br>2-bit KV 압축과 CUDA/Triton 구현은 GPU 메모리·배치 효율의 후보 편익을 보이지만, 잔여 full-precision 캐시를 포함한 금액 TCO·도입·운영비와 코드 라이선스는 제공 발췌에서 확인되지 않는다. [4, 물리 p.1] [4, 물리 p.6] [4, 물리 p.2] [4, 물리 p.8]<br><br>**조건:** KIVI 구현은 CUDA와 Triton GPU kernel을 사용한다. 논문 source_metadata는 arXiv:2402.02750v2(2024, SHA-256 df31ef32d71bfb280c533c5db8220cadf5ef42076bf45d82ba4c8da8e50ea5f), 공식 README snapshot은 version baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf(date unknown)이다. 효율 근거인 Figure 5(p7–8)는 ShareGPT synthetic workload, 평균 입력 161·출력 338토큰, Llama-2-7B, residual 32·128, FP16 baseline, 단일 A100 80GB에서 OOM까지 batch를 늘린 실제 wall-clock peak memory·throughput 비교이며, 최대 4× batch·2.35×∼3.47× throughput을 보고한다. 반복 횟수·software 세부·절대 batch·기업업무 비용 전환은 미확인이다.<br><br>**한계:** 제공 자료에서 금전적 CAPEX/OPEX, cloud·on-premise 가격, 통합 인력, support 조건, 독립 재현·production 운용과 기업 문서 정확도 검증은 확인되지 않는다. CUDA/Triton과 실험실 메모리 효율은 비용 절감의 직접 금액 근거가 아니며, residual cache가 full precision이라는 구현 조건도 남는다. 제공 코드 발췌의 license 문구 미확인은 라이선스 부재가 아니다. | **미확인 · market-6**<br><br>CPU KV 풀·동적 prefetch와 partial weights는 GPU·전송 자원 절감의 후보 편익이지만, CPU/DRAM·PCIe·예측 오버헤드를 포함한 금액 TCO·통합·운영비와 라이선스는 제공 발췌에서 확인되지 않는다. [2, 물리 p.1] [2, 물리 p.2] [2, 물리 p.13] [2, 물리 p.9] [3, snapshot block 8, character 0]<br><br>**조건:** 논문 source_metadata는 arXiv:2406.19707v1(2024, SHA-256 267d689a1ded953f076eb93976c0ebeac1ad02029f1f7c9dd1c947aa05d7cb5f), 공식 README snapshot은 version f6a08e32c16d3fdbe8839a95775f2b1e2a2690e36e6ee9d8ec683d6c24e89a90(date unknown)이다. Figure 16(b)의 알려진 속도 비교는 OPT 6.7B·13B·30B, 입력 1,920·출력 128토큰, batch 4, RTX A6000 48GB, Intel Xeon Gold 6136, DDR4-2666 96GB, PCIe 3.0×16에서 INT4·H2O·InfiniGen의 FlexGen 대비 speedup이며, 논문은 해당 장비에서 실행한 실험으로 기술하지만 반복 횟수·software version·wall-clock 측정 프로토콜·데이터셋과 InfiniGen 정밀도는 발췌에서 미확인이다. Figure 17은 alpha=4에서 partial-weight ratio를 조정한 accuracy·latency 실험이고 ratio=0.3을 선택하지만, 모델·정밀도·입출력 길이·batch·장비·데이터셋·baseline·측정/시뮬레이션 여부는 미확인이다. Table 2의 80% eviction perplexity는 별도 memory-limit 정책 실험이다.<br><br>**한계:** CPU/DRAM·PCIe, partial weights와 prediction은 논문 구조에서 추론되는 자원 항목이지 가격 근거가 아니다. Figure 17의 ratio 증가는 partial-weight·key-cache memory overhead를 키우지만 금액 절감으로 환산되지 않으며, selective prefetch의 무손실성이나 기업 문서업무 비용 효과도 확인되지 않는다. 제공 코드 발췌에서 저장소 license 문구가 확인되지 않는 것은 라이선스 부재를 뜻하지 않는다. |

# 이해관계자

| 비교 질문 | KIVI | InfiniGen |
| --- | --- | --- |
| 문서 검토자 | **적용 가정 · stakeholder-1**<br><br>문서 검토자 관점의 장문·반복·동시 요청 시나리오에서 KIVI는 GPU 메모리와 batch 여지를 넓힐 수 있지만, 잔여 캐시는 full precision이고 기업 문서 품질과 결과 대조 부담은 아직 검증되지 않았다. [1, snapshot block 15, character 0] [4, 물리 p.2] [4, 물리 p.7] [4, 물리 p.8] [4, 물리 p.9]<br><br>**조건:** KIVI arXiv:2402.02750v2(2024) p7–8 Figure 5는 Llama-2-7B, 논문상 2-bit KIVI와 FP16 baseline, residual length 32·128, ShareGPT 기반 synthetic workload(평균 input 161/output 338 tokens)를 사용했다. OOM까지 batch를 늘려 peak memory·throughput·maximum batch size를 wall-clock으로 비교했으며, 단일 NVIDIA A100 80GB에서 유사 maximum memory 기준 최대 4× batch와 2.35×–3.47× throughput을 보고했다. Figure 5의 KIVI-2/KIVI-4 variant별 정밀도·절대 batch·latency·accuracy·반복·software 설정은 검색 발췌에서 미확인이다. LongBench는 일반 benchmark의 부분 확인일 뿐 기업 문서·Agentic tool-call 결과는 unknown이다.<br><br>**한계:** 공개 AiPMO 업무 설명과 SK AX의 장문·반복·동시 요청 분석 가정을 KIVI 실험에 연결한 시나리오이지, 실제 사용자 인터뷰·도입·기업 문서 결과가 아니다. 잔여 key/value cache는 full precision이므로 전체 캐시가 모두 2-bit인 것도 아니다. | **적용 가정 · stakeholder-4**<br><br>문서 검토자 관점의 장문 요청 시나리오에서 InfiniGen은 CPU KV pool과 필요한 항목의 동적 prefetch로 GPU 압박을 낮출 여지가 있지만, 선택적 가져오기를 무손실로 단정할 수 없고 조항 보존·문서 품질은 미검증이다. [1, snapshot block 15, character 0] [2, 물리 p.1] [2, 물리 p.2] [2, 물리 p.11]<br><br>**조건:** InfiniGen arXiv:2406.19707v1(2024) p1–2의 CPU KV pool·동적 prefetch 구조를 AiPMO의 RFP·계약 검토 설명에 연결한 시나리오이며, 기업 조항 보존 결과가 아니다. p11 Table 2는 sequence length 2048의 WikiText-2·PTB perplexity(lower is better)를 OPT-6.7B·13B·30B와 Llama-2-7B·13B에서 100%와 80% KV-cache memory limit의 FIFO·LRU·Counter 축출 정책으로 비교한다. OPT-13B의 100%는 Wiki/PTB 10.55/12.78, 80-FIFO는 30.99/33.84, 80-LRU·Counter는 각각 10.55/12.78이다. 정밀도·input/output 분리 길이·batch·장비·측정/시뮬레이션 여부는 검색 발췌에서 미확인이다. 이 표는 축출 정책 perplexity 실험이지 selective prefetch 또는 기업 문서 정확도 검증이 아니며 target workload는 unknown이다.<br><br>**한계:** CPU pool과 selective prefetch는 장문 생성의 GPU 메모리 부담을 줄일 수 있는 설계·적용 시나리오로 해석되지만, full-cache와 수학적으로 동일하거나 무손실이라는 보장은 제공 발췌에서 확인되지 않는다. Table 2의 80% 축출 결과를 selective prefetch의 기업 문서 품질 결과로 귀속하지 않는다. |
| AI·인프라 운영자 | **팀 추론 · stakeholder-2**<br><br>AI 운영자는 KIVI의 CUDA/Triton 커널과 full-precision 잔여 캐시를 관측하고 group size·residual length를 조정해야 한다. A100 wall-clock 효율은 확인됐지만 문서 SLO·동시성·반복운영은 미검증이다. [4, 물리 p.6] [4, 물리 p.2] [4, 물리 p.7] [4, 물리 p.8]<br><br>**조건:** KIVI p6은 CUDA 기반 dequantization·matrix multiplication fusion, Triton group-wise kernel과 weight-only 호환을 설명한다. p7 Table 5 ablation은 Llama2-13B의 GSM8K에서 group size 32·64·128 및 residual length 32·64·96·128을 비교하며, group size 128의 성능 저하와 잔여 길이별 일관되지 않은 정확도 패턴을 보고한다. 이 ablation의 정밀도·장비·batch·입출력 길이·반복·software 설정은 검색 발췌에서 미확인이다. 별도로 p7–8 Figure 5의 실제 wall-clock 결과는 Llama-2-7B, 2-bit KIVI/FP16 baseline, ShareGPT synthetic workload(평균 input 161/output 338), residual length 32·128, 단일 A100 80GB, OOM까지 batch 증가, peak memory·throughput·maximum batch 비교 조건이며, 반복 횟수와 software 세부는 미확인이다. 기업 문서 SLO·동시성·장애·품질 관측 기준은 unknown이다.<br><br>**한계:** CUDA/Triton 통합, full-precision 잔여 캐시의 관측, group·residual 조정 필요성은 기술 구조와 조건부 실험에서 도출한 팀 해석이다. 그룹·잔여 길이 민감도는 모든 모델이나 기업 문서업무의 보편적 결과가 아니며, production 운용은 검색 발췌에서 확인되지 않는다. | **팀 추론 · stakeholder-5**<br><br>AI 운영자는 InfiniGen의 동적 prefetch와 CPU–GPU 전송을 관측하면서 alpha·partial-weight ratio·메모리 overhead를 조정해야 한다. Figure 17의 latency/accuracy sweep은 확인됐지만 문서 SLO와 동시성 우위는 미검증이다. [2, 물리 p.2] [2, 물리 p.12] [2, 물리 p.13] [2, 물리 p.9]<br><br>**조건:** p12 Figure 17은 alpha와 partial weight ratio별 accuracy·inference latency를 보인다. p13은 partial-ratio sweep을 alpha 4에서 수행하고 ratio 0.3을 선택했으며, ratio 증가에 따른 partial weights·key cache memory overhead와 0.3 초과에서 뚜렷하지 않은 accuracy 차이를 설명한다. 그러나 Figure 17의 모델·정밀도·input/output 길이·batch·장비·데이터셋·baseline·측정/시뮬레이션·반복은 검색 발췌에서 미확인이다. 별도 Figure 16(b)는 OPT 6.7B·13B·30B, input 1,920/output 128, batch 4에서 INT4·H2O·InfiniGen의 FlexGen 대비 speedup을 비교하며, RTX A6000 48GB·Xeon Gold 6136·DDR4-2666 96GB·PCIe 3.0×16 환경이 확인된다. 이 Figure 16(b)의 InfiniGen 정밀도·데이터셋·측정/시뮬레이션·반복과 기업 문서 SLO·동시성은 unknown이며 Figure 17 조건과 합치지 않는다.<br><br>**한계:** alpha·partial-weight ratio 조정과 CPU–GPU 전송·메모리 관측을 운영 부담으로 보는 것은 팀 해석이다. Figure 17의 sweep은 기업 문서업무 검증이 아니며 Table 2의 축출 실험과도 다르므로, 특정 SLO나 운영 우위를 단정할 수 없다. |
| 구매·보안·관리 담당자 | **팀 추론 · stakeholder-3**<br><br>구매·보안·책임 담당자는 KIVI 논문과 공식 저장소를 식별할 수 있지만, 제공 발췌에서 코드 license 문구와 기업 문서 독립 재현은 확인되지 않았다. 사용권·보안·오류 책임·검수기준은 별도 확정이 필요하다. [4, 물리 p.1] [4, 물리 p.6] [4, 물리 p.9]<br><br>**조건:** source_metadata상 논문은 arXiv:2402.02750v2(2024), SHA-256 df31ef32d71bfb280c533c5db8220cadf5ef42076bf45d82ba4c8da8e50ea5f4이다. KIVI official repository README snapshot version은 baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf이며 date는 unknown이다. 확인 범위는 Llama/Llama-2·Falcon·Mistral, LongBench·생성 과제, CUDA/Triton GPU 구현이다. Falcon multi-query attention의 Table 3은 16-bit·4-bit·2-bit와 CoQA·TruthfulQA·GSM8K 조건을 다루지만, 해당 발췌의 장비·batch·반복·software 설정과 기업 문서 독립 재현·배포·접근통제·책임·검수 기준은 unknown이다. license는 검색 미확인이다.<br><br>**한계:** 제공된 검색 발췌에서 license 문구가 확인되지 않는다는 뜻이지 라이선스 부재를 의미하지 않는다. 논문·저장소 식별과 공개 benchmark는 사용권, 데이터보호, 기업 문서 오류의 책임경계 또는 production 적합성을 확정하지 않으며, 이 관점 비교는 실제 인터뷰 결과가 아니다. | **팀 추론 · stakeholder-6**<br><br>구매·보안·인프라·책임 담당자는 CPU에 KV pool을 두는 설계와 논문·저장소를 식별할 수 있지만, 제공 발췌에서 license·접근통제·보존·독립 재현은 확인되지 않았다. 데이터 이동과 오류 책임·검수기준은 별도 확인이 필요하다. [2, 물리 p.1] [2, 물리 p.2] [2, 물리 p.9]<br><br>**조건:** source_metadata상 논문은 arXiv:2406.19707v1(2024), SHA-256 267d689a1ded953f076eb93976c0ebeac1ad02029f1f7c9dd1c947aa05d7cb5f이다. InfiniGen official repository README snapshot version은 f6a08e32c16d3fdbe8839a95775f2b1e2a2690e36e6ee9d8ec683d6c24e89a90이며 date는 unknown이다. p1–2의 CPU KV pool·동적 prefetch와 p9의 RTX A6000–Xeon–PCIe 환경은 확인되지만, 제공 발췌에서 저장소 license, CPU KV 접근통제·보존정책, GPU·CPU 이동의 보안 통제, 독립 재현·배포 검증, 기업 문서 오류 책임·검수기준은 unknown이다.<br><br>**한계:** CPU KV pool 배치와 CPU–GPU 이동은 보안 위반으로 확인된 것이 아니라 구매·보안·인프라 검토가 필요한 설계 조건이다. license 문구가 검색되지 않는다는 것은 라이선스 부재가 아니며, 이 관점 비교는 실제 담당자 인터뷰 결과가 아니다. |

# 도메인 적용

| 비교 질문 | KIVI | InfiniGen |
| --- | --- | --- |
| 적합 조건 | **적용 가정 · domain-1**<br><br>RFP·계약·사업계획서·발주 문서를 검토하고 반복 업무를 Agent가 수행하는 시나리오에서 KIVI는 KV 메모리 절감 후보지만, 문서 사실성·근거 인용·도구호출 지연과 동시성 적합성은 아직 unknown이다. [1, snapshot block 15, character 0] [1, snapshot block 17, character 0] [4, 물리 p.8] [4, 물리 p.2]<br><br>**조건:** 도메인 근거는 AiPMO 공개 snapshot(source_metadata version 6dbb089c1432e38eaf7f5d93f2d7fa2b4a03ef31a35c9878463f4589f6d77997, date unknown)이다. 장문·반복·동시 요청과 Agent 도구호출은 팀의 적용 가정이다. KIVI arXiv:2402.02750v2 p7–8 Figure 5의 효율 anchor는 Llama-2-7B, KIVI residual length 32·128, FP16 baseline, ShareGPT 기반 synthetic workload(평균 input 161/output 338 tokens), batch를 out-of-memory까지 증가, 단일 NVIDIA A100 80GB, wall-clock peak memory·throughput·max batch 비교다. 유사 maximum memory에서 최대 4× batch와 2.35×–3.47× throughput을 보고했다. 실제 장비 wall-clock 비교는 확인되지만 KIVI-2/KIVI-4 precision mapping, absolute batch, latency·accuracy, 반복 횟수·software detail 및 명시적 simulation 여부는 검색 발췌에서 미확인이다. 논문은 KIVI를 2-bit 방식으로 제시하되 key는 per-channel, value는 per-token으로 처리한다.<br><br>**한계:** AiPMO 공개 설명과 KIVI 논문 조건을 연결한 적용 시나리오이지 기업 문서업무의 결과가 아니다. KIVI의 2-bit 표기는 전체 KV가 2-bit라는 뜻이 아니며, grouped cache만 양자화하고 residual key/value와 local sliding window는 full precision으로 유지한다. SK AX 내부 구조·채택, 문서 정확도, 도구호출 연계·보안은 제공 자료 범위에서 확인되지 않는다. | **적용 가정 · domain-4**<br><br>RFP·계약·사업계획서·발주 문서를 장문으로 검토하는 Agentic AI에서 InfiniGen은 CPU KV pool과 GPU 선택적 prefetch를 쓰는 메모리 계층 후보지만, 문서 정확도·도구호출 지연·동시 요청 적합성은 아직 unknown이다. [1, snapshot block 15, character 0] [2, 물리 p.1] [2, 물리 p.2]<br><br>**조건:** InfiniGen arXiv:2406.19707v1 p1–2의 구조는 modern offloading-based inference system을 전제로 한다. Prefill에서 partial weights를 만들고 decoding의 Layer i−1에서 다음 Layer i attention을 추정한 뒤 CPU KV pool에서 필요한 항목을 GPU로 동적 prefetch한다. 실제 RFP·계약 문서의 모델·정밀도·입출력 길이·batch·CPU/GPU 구성·PCIe 조건·도구호출 흐름은 제공 자료에서 확인되지 않으며, 장문·반복·동시 요청은 팀의 적용 가정이다.<br><br>**한계:** CPU memory에 KV pool을 두고 GPU로 필요한 항목을 가져오는 오프로딩 인프라가 있는 경우를 상정한 적용 시나리오다. 선택적 prefetch가 full-cache와 수학적으로 동일하거나 무손실이라는 보장은 제공 근거에서 확인되지 않는다. 기업 문서의 정확도·지연·동시성·도구호출·보안 적합성 및 InfiniGen 채택 사실은 제공 자료에서 확인되지 않는다. |
| 정확도·운영 위험 | **저자 보고 결과 · domain-2**<br><br>KIVI 저비트 정확도는 모델·attention 구조와 group/residual 설정에 민감하다. Falcon multi-query에서는 논문이 4-bit 정확도 유지와 2-bit 큰 하락 가능성을 보고했다. [4, 물리 p.6] [4, 물리 p.7]<br><br>**조건:** 문서 기준은 arXiv:2402.02750v2 Table 3·Table 5(p6–7)이다. Table 3은 Falcon multi-query에서 16-bit·4-bit·2-bit를 CoQA·TruthfulQA·GSM8K에 비교한다. Table 5는 Llama2-13B의 GSM8K에서 group size 32·64·128 및 residual length 32·64·96·128을 비교한다. 모델의 정확한 크기, input/output length, batch, hardware, 반복 횟수·software 및 measurement/simulation 여부는 제공 발췌에서 미확인이다. KIVI의 full-precision KV sliding window는 논문 조건으로 확인되지만 목표 기업 문서의 품질 지표는 unknown이다.<br><br>**한계:** Falcon의 4-bit·2-bit 관찰은 multi-query attention의 논문 실험에 한정되며 모든 모델이나 기업 문서 검토의 보편적 결과가 아니다. group size와 residual length 관찰도 별도 ablation이므로 목표 업무의 사실성·근거 인용·리스크 recall로 일반화할 수 없다. 잔여 KV와 sliding window가 full precision으로 남는 메모리 trade-off 및 보안 영향도 별도 검증이 필요하다. | **팀 추론 · domain-5**<br><br>OPT-13B의 80-FIFO KV-cache 제한은 WikiText-2·PTB perplexity 30.99·33.84로 100%의 10.55·12.78보다 높지만, 이는 selective prefetch 손실이 아니며 alpha·부분 가중치 비율은 정확도·지연 절충을 만든다. [2, 물리 p.11] [2, 물리 p.12] [2, 물리 p.13]<br><br>**조건:** arXiv:2406.19707v1 Table 2(p11)는 sequence length 2048의 WikiText-2·PTB에서 perplexity(lower is better)를 OPT-6.7B·13B·30B와 Llama-2-7B·13B의 100%와 80-FIFO/LRU/Counter% KV-cache memory-limit·축출 정책으로 비교한다. OPT-13B의 100%는 Wiki/PTB 10.55/12.78, 80-FIFO%는 30.99/33.84다. 정밀도, input/output 분리 길이, batch, hardware, baseline 외 측정/시뮬레이션 여부는 표 발췌에서 미확인이다. Figure 17(p12)은 alpha와 partial weight ratio별 accuracy·inference latency 실험이며, p13의 ratio sweep은 alpha=4, 선택 ratio=0.3이다. Figure 17의 모델·정밀도·입출력 길이·batch·장비·dataset·baseline·정확한 측정/시뮬레이션 여부는 제공 발췌에서 미확인이다.<br><br>**한계:** Table 2의 80-FIFO·LRU·Counter는 KV cache memory limit에서의 축출 정책 비교이지 InfiniGen selective prefetch 결과가 아니다. 따라서 FIFO perplexity를 InfiniGen prefetch의 정확도 손실로 직접 귀속하지 않는다. Figure 17은 별도의 alpha·partial-weight sweep이며, 선택적 가져오기를 무손실로 단정할 수 없다. 기업 IT 문서업무에서의 정확도·지연 재현은 unknown이다. |
| 확인할 실험 | **팀 추론 · domain-3**<br><br>도입 전 동일한 RFP·계약 문서와 Agent 도구 chain에서 FP16과 KIVI를 A/B 비교해 사실성·근거 인용·리스크 recall, p50/p95 지연·peak memory·동시성별 오류와 SLO를 함께 측정해야 한다. [1, snapshot block 17, character 0] [4, 물리 p.8] [4, 물리 p.9] [4, 물리 p.6]<br><br>**조건:** 목표 실험은 같은 RFP·계약 문서, Agent prompt·tool chain, 모델·정밀도·입출력 길이·batch·장비·software에서 FP16과 KIVI를 비교하고 사실성, 근거 인용률, 리스크 recall, p50/p95 latency, peak memory, 동시성별 오류·SLO, 접근통제·보안 격리를 기록하는 설계다. 공개 효율 anchor는 arXiv:2402.02750v2 p7–8 Figure 5의 Llama-2-7B, residual 32·128, FP16, ShareGPT synthetic input/output 평균 161/338 tokens, OOM까지의 batch, 단일 A100 80GB, wall-clock peak memory·throughput·max batch 비교다. wall-clock 사실은 확인되지만 절대 batch, KIVI-2/KIVI-4 매핑, latency·accuracy, 반복 횟수·software detail 및 명시적 simulation 여부는 미확인이다. source_metadata는 논문 2402.02750v2(2024, SHA-256 df31ef32d71bfb280c533c5db8220cadf5ef42076bf45d82ba4c8da8e50ea5f4), 공식 README snapshot version baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf(date unknown)이다.<br><br>**한계:** 동일 문서·모델·정밀도·입출력 길이·batch·장비·software를 고정하는 A/B 비교와 보안 격리 측정은 제안된 검증 설계이지 보고된 기업업무 결과가 아니다. LongBench와 ShareGPT 기반 효율 결과는 RFP·계약 문서 및 Agent 도구호출을 대체하지 않는다. 제공된 코드 발췌에 license 문구가 없어 라이선스는 검색 미확인이지 부재가 아니다. | **팀 추론 · domain-6**<br><br>검증은 같은 기업 문서·prompt·모델·정밀도·입출력 길이·batch·장비에서 full-cache, 기존 offloading, InfiniGen을 A/B 비교하고, 근거 정확도·누락·p50/p95 지연·CPU/GPU 메모리·전송량·동시성 SLO를 판정해야 한다. [2, 물리 p.2] [2, 물리 p.9] [2, 물리 p.12] [1, snapshot block 17, character 0]<br><br>**조건:** 목표 실험은 동일 문서·prompt·모델·정밀도·input/output length·batch·장비·software에서 full-cache, 기존 offloading baseline과 InfiniGen을 비교하고 근거 정확도·누락, p50/p95 latency, CPU/GPU memory, CPU-GPU transfer, 동시성별 오류·SLO, 접근통제·보안 격리를 기록하는 설계다. 공개 속도 anchor는 arXiv:2406.19707v1 Section 5.1·Figure 16(b)의 OPT 6.7B·13B·30B, input 1,920/output 128 tokens, batch 4, NVIDIA RTX A6000 48GB, Intel Xeon Gold 6136·DDR4-2666 96GB, PCIe 3.0×16이다. 비교 기준은 FlexGen 대비 speedup이며 INT4·H2O·InfiniGen을 비교한다. InfiniGen 자체 정밀도, Figure 16 speedup dataset, 정확한 측정/시뮬레이션 여부, 반복 횟수와 software detail은 제공 발췌에서 미확인이다. source_metadata는 논문 2406.19707v1(2024, SHA-256 267d689a1ded953f076eb93976c0ebeac1ad02029f1f7c9dd1c947aa05d7cb5f), 공식 README snapshot version f6a08e32c16d3fdbe8839a95775f2b1e2a2690e36e6ee9d8ec683d6c24e89a90(date unknown)이다.<br><br>**한계:** 동일 기업 문서에서의 full-cache·기존 offloading·InfiniGen 비교는 제안이며 공개된 목표업무 결과가 아니다. Figure 16(b)의 speedup은 기업 문서의 사실성·근거 누락·SLO·보안 격리를 검증하지 않으며 KIVI Figure 5와 모델·길이·batch·장비·baseline이 달라 직접 순위화할 수 없다. 제공된 InfiniGen 저장소 발췌에 license 문구가 없어 라이선스는 검색 미확인이지 부재가 아니며, 독립 재현·production 운용도 unknown이다. |

# 관점 간 상충과 한계

## both · synthesis-1

**팀 추론 · synthesis-1**

KIVI의 A100·Llama-2-7B·ShareGPT wall-clock과 InfiniGen의 A6000·OPT·FlexGen 대비 speedup은 조건이 달라 기업 문서업무의 공통 우열이나 직접 순위를 제시하지 않는다. [4, 물리 p.8] [4, 물리 p.7] [4, 물리 p.2] [2, 물리 p.12] [2, 물리 p.9]

**조건:** 비교 근거는 KIVI arXiv:2402.02750v2(2024, SHA-256 df31ef32d71bfb280c533c5db8220cadf5ef42076bf45d82ba4c8da8e50ea5f4) p7–8 Figure 5와 InfiniGen arXiv:2406.19707v1(2024, SHA-256 267d689a1ded953f076eb93976c0ebeac1ad02029f1f7c9dd1c947aa05d7cb5f) Section 5.1·Figure 16(b)이다. KIVI는 Llama-2-7B, 논문상 2-bit KIVI, residual length 32·128, FP16 baseline, ShareGPT 기반 synthetic workload(평균 input 161/output 338 tokens), OOM까지 batch를 늘린 wall-clock peak memory·throughput·maximum batch, 단일 NVIDIA A100 80GB 조건이며 최대 4× batch와 2.35×–3.47× throughput을 보고했다. Figure 5의 KIVI-2/KIVI-4 정밀도 매핑, 절대 batch, latency·accuracy, 반복·software 설정과 명시적 simulation 여부는 검색 미확인이다. InfiniGen은 OPT 6.7B·13B·30B, input 1,920/output 128 tokens, batch 4, RTX A6000 48GB·Xeon Gold 6136·DDR4-2666 96GB·PCIe 3.0×16에서 INT4·H2O·InfiniGen의 FlexGen 대비 speedup을 비교했으며, InfiniGen 정밀도·dataset·반복·software와 정확한 측정/시뮬레이션 여부는 검색 미확인이다. KIVI 공식 README snapshot version은 baa1095e6edf8263bbf20507f0d1ce444c3cb57d97d5f5677c2ac19c3b934bbf(date unknown), InfiniGen 공식 README snapshot version은 f6a08e32c16d3fdbe8839a95775f2b1e2a2690e36e6ee9d8ec683d6c24e89a90(date unknown)이다.

**한계:** 두 결과의 workload·모델·정밀도·입출력 길이·batch·장비·baseline·지표가 달라 기업 IT 문서업무의 직접 우열로 해석하지 않는다. KIVI는 residual key/value를 full precision으로 유지하며, InfiniGen 선택적 prefetch도 full-cache와 동일하거나 무손실이라고 단정하지 않는다. 두 저장소의 license 문구는 제공 발췌에서 검색 미확인이지 부재가 아니며, 독립 재현·production 운용·목표 도메인 결과도 미확인이다.

## both · synthesis-2

**팀 추론 · synthesis-2**

InfiniGen의 Table 2 80% 축출 정책 perplexity와 Figure 17 alpha·부분 가중치 accuracy/latency sweep은 별도 실험이므로 selective prefetch의 무손실성이나 기업 문서 성능으로 결론낼 수 없다. [2, 물리 p.11] [2, 물리 p.12] [2, 물리 p.13] [2, 물리 p.2]

**조건:** 근거 문서는 arXiv:2406.19707v1(2024)의 Table 2(p11), Figure 17(p12), 부분 가중치 설명(p13)이다. Table 2는 sequence length 2048의 WikiText-2·PTB perplexity(lower is better)를 OPT-6.7B·13B·30B와 Llama-2-7B·13B의 100% 및 80-FIFO/LRU/Counter% KV-cache memory-limit·축출 정책으로 비교한다. OPT-13B의 Wiki/PTB는 100% 10.55/12.78, 80-FIFO 30.99/33.84, 80-LRU 10.55/12.78, 80-Counter 10.55/12.78이다. 정밀도, input/output 분리 길이, batch, 장비, 측정/시뮬레이션 여부는 발췌에서 미확인이다. Figure 17은 alpha와 partial-weight ratio별 accuracy·inference latency 실험이며, p13의 ratio sweep은 alpha=4에서 수행되고 ratio=0.3을 선택한다. 해당 sweep의 모델·정밀도·입출력 길이·batch·장비·dataset·baseline·정확한 측정/시뮬레이션 여부는 미확인이다. Table 2와 Figure 17 모두 기업 IT 문서 검토 Agentic AI의 정확도·지연 검증은 아니다.

**한계:** Table 2의 80-FIFO/LRU/Counter는 KV-cache memory limit에서의 축출 정책 비교이지 InfiniGen selective prefetch의 정확도 실험이 아니다. Figure 17도 별도의 alpha·partial-weight sweep이므로 두 결과를 하나의 무손실성 또는 기업 문서업무 결과로 결합하지 않는다. 목표 업무의 문서 정확도·지연·동시성 재현은 unknown이다.

## 남은 근거 공백

- Agentic AI가 기업 IT 사업 문서를 검토하는 실제 데이터와 에이전트 도구호출 환경에서 KIVI의 정확도·지연·동시성·운영 안정성은 unknown이다. (gap-research_kivi-1)

- Figure 5 발췌에서 절대 batch 크기, KIVI-2/KIVI-4 구분, latency·accuracy, 반복 횟수와 세부 소프트웨어 설정은 검색 미확인이다. (gap-research_kivi-2)

- 제공된 코드 발췌에는 license 문구가 없으며, 이는 라이선스 부재가 아니라 검색 미확인이다. 독립 재현과 production 운용도 unknown이다. (gap-research_kivi-3)

- 기업 IT 문서 검토 Agentic AI의 대표 사용조건에서 정확도·지연·동시성·SLO·지속운용을 검증한 공개 근거는 unknown이다. (gap-research_infinigen-1)

- 두 기술 모두 제공 자료에서 기업 IT 사업 문서를 검토하는 Agentic AI의 실제 데이터·도구호출 환경에서 정확도, 근거성·환각, latency, 동시성, SLO와 지속운용을 검증한 결과는 unknown이다. (gap-market-1)

- 제공 자료에서 공개 기업 채택·고객 사례·도입률·시장 규모와 SK AX 내부 구조 또는 KIVI·InfiniGen 채택 사실은 확인되지 않는다. 이는 제공 발췌의 검색 미확인이며 원문 전체나 비공개 도입의 부재를 뜻하지 않는다. (gap-market-2)

- CAPEX/OPEX, 클라우드·온프레미스 TCO, 통합·유지보수 인력, support 조건과 코드 저장소 license는 금액 또는 확정 조건으로 산정할 근거가 제공 발췌에서 unknown이다. (gap-market-3)

- 동일 모델·정밀도·입출력 길이·batch·장비·baseline에서 두 기술을 직접 비교한 기업 문서 검토 benchmark와 독립 재현 결과가 unknown이다. (gap-market-4)

- 제공된 검색 발췌 범위에서 두 기술이 기업 IT 사업 문서의 조항 추출 정확도·누락·환각·근거 추적·Agentic tool-call 정확도를 검증한 결과는 확인되지 않아 unknown이다. (gap-stakeholder-1)

- 장문·반복·동시 요청에서 기업 문서의 latency·SLO·동시성·장애 복구·지속운용 결과는 두 기술 모두 unknown이다. KIVI는 A100 wall-clock 효율 자체는 확인됐지만 반복 횟수와 software 세부가 남아 있다. (gap-stakeholder-2)

- KIVI Figure 5의 KIVI-2/KIVI-4 variant별 정밀도, 절대 batch, latency·accuracy, 반복·software 설정과 기업 문서 독립 재현·production 검증은 검색 발췌에서 미확인이다. (gap-stakeholder-3)

- InfiniGen Table 2의 80% 축출 정책을 selective prefetch의 문서 정확도와 연결할 수 없으며, Figure 17의 모델·정밀도·길이·batch·장비·데이터셋·baseline·측정/시뮬레이션·반복 조건은 검색 발췌에서 미확인이다. (gap-stakeholder-4)

- 두 기술의 제공 발췌에서 저장소 license 문구와 CPU KV pool의 접근통제·보존정책·데이터 이동 통제·오류 책임경계·검수기준은 unknown이다. SK AX 내부 구조와 KIVI·InfiniGen의 실제 채택·도입 여부도 제공 근거에서 확인하지 않는다. (gap-stakeholder-5)

- 제공된 AiPMO 설명과 논문 benchmark 사이에서 실제 RFP·계약·사업계획서·발주 문서와 Agent 도구 chain을 사용한 사실성·근거 인용·리스크 recall, latency, peak 또는 CPU/GPU memory, 동시성 SLO, 접근통제·보안 격리 및 생산 운용 안정성은 양 기술 모두 unknown이다. (gap-domain-1)

- KIVI Figure 5 발췌에서 절대 batch, KIVI-2/KIVI-4 정밀도 매핑, latency·accuracy, 반복 횟수·software detail 및 명시적 simulation 여부가 미확인이다. 제공된 KIVI 코드 발췌의 license 문구도 검색 미확인이며 라이선스 부재를 뜻하지 않는다. (gap-domain-2)

공백의 원문·해소 판단·근거는 [공백 검수표](gap_review.md)에 보존했습니다. 자동 판정은 실제 도입이나 모든 인용의 의미 정확성을 인증하지 않습니다.

# REFERENCE

[1] SK AX (발행일 미상). **SK AX AiPMO**. 공식 웹 자료, 스냅샷 6dbb089c1432. 조회 2026-09-21.  
https://www.skax.co.kr/ax-services/aipmo

[2] Wonbeom Lee et al (2024). **InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management**. arXiv, 2406.19707v1. 조회 2026-09-22.  
https://arxiv.org/pdf/2406.19707v1

[3] SNU Computer Architecture Lab (발행일 미상). **InfiniGen official repository README**. 공식 웹 자료, 스냅샷 f6a08e32c16d. 조회 2026-09-21.  
https://raw.githubusercontent.com/snu-comparch/InfiniGen/main/README.md

[4] Zirui Liu et al (2024). **KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache**. arXiv, 2402.02750v2. 조회 2026-09-22.  
https://arxiv.org/pdf/2402.02750v2
