# v1 Ranking Hardening

v0를 복제한 뒤 reranker, usage logs, feedback loop, baseline/candidate compare, catalog/experiment CRUD를 추가한 버전.

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
pnpm e2e
```

## Features

- candidate reranking
- usage event API
- feedback API
- experiment CRUD
- compare snapshot UI

## Status

- implemented and verified
