# v3 OSS Hardening Problem

## Problem

`v2`는 운영형 MCP 추천 시스템 데모로는 충분하지만, 다른 팀이 바로 self-hosted 도구처럼 설치해서 쓰기에는 제품 경계가 약하다. `v3`의 과제는 추천 품질을 더 높이는 것이 아니라, 아래 네 축을 추가해 single-team self-hosted OSS 후보로 만드는 것이다.

- auth/RBAC
- single-workspace product core
- background jobs + audit/metrics
- single-node compose deployment

## Fixed Scope

- local email/password auth only
- roles: `owner`, `operator`, `viewer`
- single workspace per deployment
- Postgres-backed queue via `pg-boss`
- manual import/export and CRUD only
- external live integrations는 범위 밖

## Inputs

- `shared/`의 catalog seed, eval fixtures, release candidate fixtures
- `.env.example`의 runtime variables
- Docker Compose single-node topology

## Outputs

- 로그인 가능한 Fastify API
- role-aware Next.js 운영 콘솔
- background job queue + worker
- audit log and metrics endpoints
- self-hosted install docs and OSS metadata
- presentation deck with v3 실제 사용 사례와 캡처

## Acceptance Criteria

- anonymous request가 protected route에서 `401`을 반환한다.
- viewer mutation이 `403`을 반환한다.
- owner는 user/settings를 관리할 수 있다.
- operator는 catalog/experiment/release candidate CRUD와 job 실행이 가능하다.
- eval, compare, compatibility, release gate, artifact export가 job으로 완료된다.
- `docker compose up -d --build`로 `postgres + api + worker + web`가 함께 기동된다.
- `pnpm bootstrap:owner`가 idempotent하게 동작한다.

## Verification Commands

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
pnpm build
pnpm test
pnpm test:integration
pnpm e2e
pnpm eval
pnpm compare
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
pnpm capture:presentation
```
