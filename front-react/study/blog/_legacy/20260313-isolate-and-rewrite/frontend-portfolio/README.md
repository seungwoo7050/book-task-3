# frontend-portfolio blog

`frontend-portfolio`는 내부도구형 UI와 고객-facing multi-step flow를 각각 하나씩 보여 주는 마감 트랙이다. 이 blog 레이어는 Next.js app surface, query/mutation orchestration, unit/integration/E2E 검증을 근거로 제품형 판단이 어떻게 코드로 닫히는지 추적한다.

## 이 레이어가 쓰는 근거

- 프로젝트 README, `problem/README.md`, `next/README.md`, `docs/README.md`
- `next/app/*`, `next/src/*`, `next/tests/*`, `package.json`, `next.config.ts`, `vitest.config.ts`, `playwright.config.ts`
- `git log --reverse --stat -- study/frontend-portfolio/<project>`
- 2026-03-13 재실행한 `npm run verify --workspace ...`

## 프로젝트 목록

| 프로젝트 | 최종 blog | evidence ledger | structure |
| --- | --- | --- | --- |
| Ops Triage Console | [01-ops-triage-console/10-development-timeline.md](01-ops-triage-console/10-development-timeline.md) | [01-evidence-ledger.md](01-ops-triage-console/01-evidence-ledger.md) | [02-structure.md](01-ops-triage-console/02-structure.md) |
| Client Onboarding Portal | [02-client-onboarding-portal/10-development-timeline.md](02-client-onboarding-portal/10-development-timeline.md) | [01-evidence-ledger.md](02-client-onboarding-portal/01-evidence-ledger.md) | [02-structure.md](02-client-onboarding-portal/02-structure.md) |
