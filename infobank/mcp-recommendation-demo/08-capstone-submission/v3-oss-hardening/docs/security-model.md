# 보안 모델

## 경계

`v3`는 multi-tenant SaaS가 아니라 단일 워크스페이스 self-hosted 인스턴스다. 한 배포는 한 팀을 위한 운영 콘솔을 뜻한다.

## 인증

- local email/password only
- password hashing: `argon2`
- session storage: server-side session record in Postgres
- browser transport: HttpOnly cookie

## 역할

- `owner`: user/settings 관리 포함 전체 권한
- `operator`: catalog/experiment/release candidate CRUD와 job 실행
- `viewer`: read-only

## 접근 제어

- anonymous: protected route에서 `401`
- viewer mutation: `403`
- owner-only endpoints: `/api/users`, `/api/settings`, `/api/audit-logs`

## 감사 로그 범위

- login/logout
- user CRUD
- settings update
- catalog/experiment/release candidate CRUD
- usage/feedback write
- job enqueue

## 명시적인 비목표

- SSO/OAuth
- MFA
- multi-workspace isolation
- live secret rotation
