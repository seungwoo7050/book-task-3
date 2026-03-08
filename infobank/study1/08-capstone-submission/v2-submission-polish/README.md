# v2 Submission Polish

v1를 복제한 뒤 compatibility gate, release gate, submission artifact export, dry-run pipeline, release candidate CRUD를 추가한 최종 버전.

## Included Packages

- `shared/`: Zod contracts, seeded catalog, offline eval fixtures
- `node/`: Fastify + Drizzle + PostgreSQL API
- `react/`: Next.js dashboard
- `docs/`: stable runbook and proof docs
- `problem/`: fixed scope and acceptance summary

## Commands

```bash
pnpm install
cp .env.example .env
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

## Features

- release candidate CRUD
- compatibility gate
- release gate
- artifact export
- changesets + GitHub Actions dry-run

## Status

- implemented and verified
