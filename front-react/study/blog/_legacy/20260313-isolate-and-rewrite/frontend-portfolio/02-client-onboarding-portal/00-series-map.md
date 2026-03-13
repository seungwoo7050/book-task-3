# Series Map — 02 Client Onboarding Portal

## 프로젝트 경계

- 트랙: `frontend-portfolio`
- 프로젝트 루트: `study/frontend-portfolio/02-client-onboarding-portal`
- 독립 프로젝트 판정 근거: `README.md`, `problem/README.md`, `next/README.md`, `npm run verify --workspace @front-react/client-onboarding-portal`가 있고, route/portal components, lib helpers, tests가 독립 경계를 이룬다.
- 기존 blog 처리: `isolate-and-rewrite`, 기존 `study/blog/frontend-portfolio/02-client-onboarding-portal`는 없어서 새로 만들었다.

## source of truth

- 포함: 프로젝트 README, `problem/README.md`, `docs/README.md`, `next/README.md`, `next/app/*`, `next/src/components/portal/*`, `next/src/lib/*`, `next/tests/*`, `package.json`, `git log`, 2026-03-13 재검증 CLI
- 제외: `notion/**`, 이번 batch에서 생성한 `study/blog/**`

## chronology 복원 메모

- 2026-03-08 `46051f3`에서 route/app surface, portal component, guards/storage/service helpers, tests가 함께 landing했고, 2026-03-12 `0e12fb8`에서 README/problem/docs wording이 정리됐다.
- chronology는 `product surface -> route/session gate -> draft/submit retry -> verify` 순서로 복원하는 편이 코드와 시나리오 모두에 맞는다.
- 한 줄 답: sign-in, onboarding wizard, draft restore, submit retry를 갖춘 Next.js client onboarding 포털이다.

## canonical CLI

```bash
cd study
npm run verify --workspace @front-react/client-onboarding-portal
```

## series

1. [01-evidence-ledger.md](01-evidence-ledger.md)
2. [02-structure.md](02-structure.md)
3. [10-development-timeline.md](10-development-timeline.md)
