# v0 Initial Demo

registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable 데모.

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
pnpm dev
pnpm test
pnpm eval
pnpm e2e
```

## Features

- catalog list/detail
- manifest validate
- baseline recommendation
- offline eval
- Next.js dashboard

## Status

- implemented and verified
