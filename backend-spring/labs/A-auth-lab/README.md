# A-auth-lab

- Status: `verified scaffold`
- Focus: local account auth, refresh rotation, cookie patterns, and recovery flows
- Spring workspace: [spring/README.md](/Users/woopinbell/work/web-pong/study2/labs/A-auth-lab/spring/README.md#L1)

## Scope

- local signup and login
- password hashing and reset flow modeling
- refresh token rotation pattern
- HttpOnly cookie and CSRF discussion
- Mailpit-ready local email workflow

## Validation target

- `spring/` should pass `make lint`, `make test`, and `make smoke`
- `spring/compose.yaml` should boot app, PostgreSQL, Redis, and Mailpit
