# 04 baseline selector와 reranking

baseline selector를 먼저 세우고 reranker와 compare runner를 더해 추천 로직 개선을 설명 가능한 형태로 만드는 단계다.

## 이 단계에서 배우는 것

- baseline selector에서 출발해 reranker로 확장하는 법
- candidate와 baseline을 같은 입력셋에서 비교하는 실험 구조
- 추천 개선을 코드와 문서 둘 다에서 설명하는 방법

## 먼저 읽을 순서

- `problem/README.md`
- `docs/README.md`
- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/compare-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/tests/rerank-service.test.ts`

## 현재 상태

- baseline은 `v0`, reranker와 compare는 `v1`에서 구현돼 있다.
- 이 stage는 추천 품질 개선을 어디서 확인하면 되는지 길을 잡아 준다.

## 포트폴리오로 가져갈 것

- baseline 대비 candidate 개선을 설명하는 구조
- reranking 실험을 문서와 테스트로 함께 남기는 방식
