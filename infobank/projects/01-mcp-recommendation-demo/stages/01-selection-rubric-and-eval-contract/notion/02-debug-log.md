# 01 추천 품질 기준과 평가 계약 디버그 기록

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
- 이 단계는 '어떻게 구현했는가'보다 '무엇을 좋은 추천으로 볼 것인가'를 먼저 설명한다.

## 현재 상태 메모

- 실제 계약은 `v0`의 shared contract와 eval service에 반영돼 있다.
- 이 stage는 별도 구현보다 평가 기준을 stable index로 남기는 역할을 맡는다.

## 재현 실패 시 다시 볼 경로

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/eval.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/eval-service.ts`
