# v1 Ranking Hardening Problem

## Scope

v0를 복제한 뒤 reranker, usage logs, feedback loop, baseline/candidate compare, catalog/experiment CRUD를 추가한 버전.

## Acceptance Criteria

- candidate reranking
- usage event API
- feedback API
- experiment CRUD
- compare snapshot UI

## Verification Commands

```bash
pnpm install
pnpm db:up
pnpm migrate
pnpm seed
pnpm dev
pnpm test
pnpm e2e
```
