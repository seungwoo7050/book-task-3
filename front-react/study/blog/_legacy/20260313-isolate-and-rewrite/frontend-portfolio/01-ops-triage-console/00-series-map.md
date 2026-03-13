# Series Map — 01 Ops Triage Console

## 프로젝트 경계

- 트랙: `frontend-portfolio`
- 프로젝트 루트: `study/frontend-portfolio/01-ops-triage-console`
- 독립 프로젝트 판정 근거: `README.md`, `problem/README.md`, `next/README.md`, `npm run verify --workspace @front-react/ops-triage-console`가 있고, Next app, hooks/lib, unit/integration/E2E tests가 모두 독립 경계를 이룬다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/frontend-portfolio/01-ops-triage-console`는 없어서 새로 만들었다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `docs/README.md`, `next/README.md`, `next/app/*`, `next/src/hooks/use-ops-triage.ts`, `next/src/components/console/ops-triage-console.tsx`, `next/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번 batch에서 생성한 `study/blog/**`

## chronology 복원 메모

- 2026-03-08 `46051f3`에서 Next app, query/mutation hooks, UI components, tests, 발표 자료까지 한 번에 landing했고, 2026-03-12 `0e12fb8`에서 README/problem/docs wording이 다듬어졌다.
- chronology는 `product surface -> optimistic mutation -> dense console workflow -> verify` 순서로 복원하는 편이 source와 tests 둘 다에 잘 맞는다.
- 한 줄 답: dashboard, queue, bulk action, optimistic update, rollback, retry를 갖춘 Next.js 운영 triage 콘솔이다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/ops-triage-console
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
