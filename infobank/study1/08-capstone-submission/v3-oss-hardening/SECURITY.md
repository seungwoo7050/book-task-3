# Security Policy

`v3-oss-hardening`은 study-first self-hosted candidate다. production-ready 보안 보증을 제공하지는 않지만, 아래 범위는 현재 구현에 포함된다.

## Included

- email/password auth
- argon2 password hashing
- server-side session with HttpOnly cookie
- role-based route guard: `owner`, `operator`, `viewer`
- audit log for login/logout, user/settings changes, CRUD, job enqueue

## Not Included

- SSO/OAuth
- MFA
- rate limiting
- secret rotation automation
- multi-tenant isolation
- external secret manager integration

## Reporting

이 study repository 안에서 보안 이슈를 발견했다면, public issue에 민감한 exploit detail을 그대로 올리지 말고 재현 조건과 영향 범위를 최소한으로 요약해 전달하는 것을 권장한다.

## Safe Deployment Assumptions

- single team only
- private network 또는 로컬 환경
- reverse proxy와 TLS termination은 외부에서 구성
- 기본 seed 계정 비밀번호는 부트스트랩 후 즉시 변경
