# Security Model

## Boundary

`v3`는 multi-tenant SaaS가 아니라 single-workspace self-hosted 인스턴스다. 한 배포가 한 팀을 위한 운영 콘솔을 뜻한다.

## Auth

- local email/password only
- password hashing: `argon2`
- session storage: server-side session record in Postgres
- browser transport: HttpOnly cookie

## Roles

- `owner`: user/settings 관리 포함 전체 권한
- `operator`: catalog/experiment/release candidate CRUD와 job 실행
- `viewer`: read-only

## Route Guard

- anonymous: protected route에서 `401`
- viewer mutation: `403`
- owner-only endpoints: `/api/users`, `/api/settings`, `/api/audit-logs`

## Audit Coverage

- login/logout
- user CRUD
- settings update
- catalog/experiment/release candidate CRUD
- usage/feedback write
- job enqueue

## Explicit Non-Goals

- SSO/OAuth
- MFA
- multi-workspace isolation
- live secret rotation
