# v2 Submission Polish Problem

## Scope

v1를 복제한 뒤 compatibility gate, release gate, submission artifact export, dry-run pipeline, release candidate CRUD를 추가한 최종 버전.

## Acceptance Criteria

- release candidate CRUD
- compatibility gate
- release gate
- artifact export
- changesets + GitHub Actions dry-run

## Verification Commands

```bash
pnpm install
pnpm db:up
pnpm migrate
pnpm seed
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
pnpm test
pnpm e2e
```
