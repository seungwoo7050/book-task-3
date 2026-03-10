# 03 차별화 포인트와 노출 설계 디버그 기록

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
- 이 단계는 ranking 수치 자체보다, 추천 이유를 어떻게 표현할지를 다룬다.

## 현재 상태 메모

- 실제 노출 문구와 reason template은 `v0`에서 구현되고 이후 버전이 그대로 재사용한다.
- 이 stage는 '왜 이 추천이 좋은가'를 말하는 문장을 정리하는 인덱스다.

## 재현 실패 시 다시 볼 경로

- `08-capstone-submission/v0-initial-demo/shared/src/catalog.ts`
- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v0-initial-demo/react/components/mcp-dashboard.tsx`
