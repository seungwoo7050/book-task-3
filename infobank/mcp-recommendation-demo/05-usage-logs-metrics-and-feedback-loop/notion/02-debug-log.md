# 05 로그, 지표, 피드백 루프 디버그 기록

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
- 이 단계는 추천 품질을 '사용 이후'까지 추적하는 구조를 다룬다.

## 현재 상태 메모

- usage event와 feedback loop는 `v1`에서 구현되고 `v2`가 이를 바탕으로 제출 산출물을 만든다.
- 이 stage는 운영형 추천 시스템으로 넘어가는 지점을 설명한다.

## 재현 실패 시 다시 볼 경로

- `08-capstone-submission/v1-ranking-hardening/node/src/db/schema.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/app.ts`
- `08-capstone-submission/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
