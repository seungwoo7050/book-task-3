# Next.js 구현

상태: `verified`

## 이 구현이 답하는 범위

- dashboard summary와 triage queue
- saved view, bulk action, detail action
- optimistic update, rollback, retry
- unit, integration, E2E 검증

## 핵심 파일

- `app/`: App Router 엔트리와 route 구성
- `src/components/console/ops-triage-console.tsx`: main console UI
- `src/hooks/use-ops-triage.ts`: query/mutation/runtime orchestration
- `tests/`: unit, integration, E2E 검증

## 실행과 검증

```bash
cd study
npm run dev --workspace @front-react/ops-triage-console
npm run verify --workspace @front-react/ops-triage-console
```

## 현재 한계

- mock API와 local persistence 기준 데모다.
- 실제 인증, 실제 DB, 멀티유저 협업은 없다.
- 도메인 폭은 운영 triage에 집중한다.
