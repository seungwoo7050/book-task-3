# 04 baseline selector와 reranking 지식 인덱스

## 핵심 개념

- baseline selector에서 출발해 reranker로 확장하는 법
- candidate와 baseline을 같은 입력셋에서 비교하는 실험 구조
- 추천 개선을 코드와 문서 둘 다에서 설명하는 방법

## 다시 찾을 경로

- `README.md`
- `problem/README.md`
- `docs/README.md`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/tests/rerank-service.test.ts`

## 포트폴리오 메모

- baseline 대비 candidate 개선을 설명하는 구조
- reranking 실험을 문서와 테스트로 함께 남기는 방식
