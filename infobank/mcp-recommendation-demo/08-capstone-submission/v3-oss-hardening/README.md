# v3 OSS Hardening

`v3-oss-hardening`은 `v2-submission-polish`를 self-hosted OSS 후보로 끌어올린 제품화 확장 버전이다. 목표는 새 추천 기능을 더 넣는 것이 아니라, 한 팀이 직접 설치해서 로그인된 권한 아래 catalog, experiment, release candidate, release gate를 운영할 수 있게 만드는 것이다.

`v2`는 여전히 최종 capstone demo이고, `v3`는 그 위에 얹은 productization extension이다.

## What You Can Do

- 이메일/비밀번호 로그인과 `owner | operator | viewer` 권한으로 콘솔을 구분할 수 있다.
- MCP catalog를 import/export하고 CRUD로 직접 운영할 수 있다.
- baseline/candidate 추천은 즉시 실행하고, eval/compare/compatibility/release gate/artifact export는 background job으로 안전하게 실행할 수 있다.
- audit log, job activity, latest artifact preview로 운영 흔적을 추적할 수 있다.
- `docker compose up -d --build` 한 번으로 `postgres + api + worker + web`를 single-node 환경에 올릴 수 있다.

## Package Layout

- `shared/`: Zod contracts, seed catalog, offline eval fixtures
- `node/`: Fastify API, auth/session, RBAC, pg-boss worker, Drizzle/PostgreSQL
- `react/`: Next.js 운영 콘솔
- `problem/`: v3 범위와 acceptance criteria
- `docs/`: install, security, operations, API, backup/restore, proof, 발표 문서
- `notion/`: local-only technical notebook

## Default Accounts

- `owner@study1.local / ChangeMe123!`
- `operator@study1.local / Operator123!`
- `viewer@study1.local / Viewer123!`

`pnpm bootstrap:owner`는 환경변수 `BOOTSTRAP_OWNER_EMAIL`, `BOOTSTRAP_OWNER_PASSWORD`를 읽어 owner 계정을 idempotent하게 보정한다.

## Quick Start

### Local

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
pnpm dev
```

- Web: `http://127.0.0.1:3003`
- API: `http://127.0.0.1:3103`

### Compose

```bash
docker compose up -d --build
```

Compose는 `postgres + api + worker + web`를 함께 올리고, API 컨테이너에서 migration을 적용한 뒤 서버를 시작한다.

## Verification

```bash
pnpm build
pnpm test
pnpm test:integration
pnpm eval
pnpm compare
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
pnpm e2e
pnpm capture:presentation
```

## Status

- Auth/RBAC: implemented
- Single-workspace settings: implemented
- Background jobs and audit log: implemented
- Compose packaging: implemented
- Docs, runbook, and presentation assets: implemented

## Non-Goals

- multi-workspace SaaS
- SSO/OAuth
- live GitHub or package registry sync
- webhook ingest

## Test Note

- `pnpm test`는 unit/UI test를 실행한다.
- `pnpm test:integration`은 Postgres가 준비된 상태에서만 실행하는 DB-backed route/job test다.
