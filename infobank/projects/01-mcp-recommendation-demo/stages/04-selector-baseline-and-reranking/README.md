# 04 baseline selector와 reranking

## 이 stage의 문제

baseline selector를 먼저 세우고 reranker와 compare runner를 더해 추천 로직 개선을 설명 가능한 형태로 만든다.

## 입력/제약

- 입력: baseline score, signal feature, compare 대상 버전
- 제약: baseline과 candidate를 같은 입력셋에서 비교할 수 있어야 한다.

## 이 stage의 답

- baseline selector와 reranker를 분리해 개선 근거를 남긴다.
- compare runner를 통해 candidate가 왜 더 나은지 설명할 구조를 잡는다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/tests/rerank-service.test.ts`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- `v1-ranking-hardening/node/tests/rerank-service.test.ts`가 baseline 대비 rerank 동작을 어떻게 고정하는지 확인한다.

## 현재 한계

- signal 품질은 seed data와 usage log 품질에 의존한다.
- release 판단은 아직 이 stage 범위에 없다.
