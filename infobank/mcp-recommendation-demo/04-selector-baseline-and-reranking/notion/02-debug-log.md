# 04 baseline selector와 reranking 디버그 기록

## 먼저 확인할 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm dev
pnpm test
pnpm eval
pnpm capture:presentation
pnpm e2e
```

## 다시 막히기 쉬운 지점

- 상위 `README.md`, `problem/README.md`, `docs/README.md`, 연결된 capstone 경로 설명이 서로 어긋나지 않는지 먼저 확인한다.
- `v1-ranking-hardening`가 아니라 다른 버전의 코드를 보고 있으면 stage 목적이 흐려질 수 있다.
- 이 단계는 '더 똑똑한 추천'을 만들었다는 주장보다, 왜 그렇게 판단할 수 있는지의 근거를 정리한다.

## 현재 상태 메모

- baseline은 `v0`, reranker와 compare는 `v1`에서 구현돼 있다.
- 이 stage는 추천 품질 개선을 어디서 확인하면 되는지 길을 잡아 준다.

## 재현 실패 시 다시 볼 경로

- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/services/compare-service.ts`
- `08-capstone-submission/v1-ranking-hardening/node/tests/rerank-service.test.ts`
