# A-auth-lab

- Status: `verified`
- Focus: local account authentication with cookie sessions and recovery flows
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/labs/A-auth-lab/fastapi/README.md#L1)

## Scope

- local signup and login
- Argon2 password hashing
- email verification
- password reset
- rotating refresh tokens
- secure cookie auth
- CSRF validation
- Mailpit-ready local email workflow

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` boots with PostgreSQL, Redis, and Mailpit
- local schema is auto-created on app startup for study convenience

## Intentional Simplifications

- email delivery is local-only and inspected through Mailpit
- tests use SQLite for speed even though Compose uses PostgreSQL
- OAuth and second-factor flows are intentionally moved to `B-federation-security-lab`
