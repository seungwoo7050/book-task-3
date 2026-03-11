# 02 registry catalog와 manifest schema 디버그 기록

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
- `v0-initial-demo`가 아니라 다른 버전의 코드를 보고 있으면 stage 목적이 흐려질 수 있다.
- 여기서는 추천 알고리즘보다 입력 데이터의 안정성과 검증 가능성을 먼저 설명한다.

## 현재 상태 메모

- 실제 schema와 seed는 `v0`에 구현돼 있고, `v1`과 `v2`가 이를 확장해 재사용한다.
- 이 stage는 데이터를 어떻게 고정했는지 설명하는 문서 단계다.

## 재현 실패 시 다시 볼 경로

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/scripts/seed.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/tests/manifest-validation.test.ts`
