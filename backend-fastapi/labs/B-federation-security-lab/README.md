# B-federation-security-lab

- Status: `verified`
- Focus: Google OAuth, external identity linking, TOTP 2FA, recovery codes, throttling, and auth audit logs
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/labs/B-federation-security-lab/fastapi/README.md#L1)

## Scope

- Google OIDC authorization-code flow
- provider-linked internal identities
- TOTP enrollment and verification
- recovery code rotation
- login throttling and auth audit trails

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` now boots against a matching PostgreSQL database name and passes live/ready probes
- local run path applies Alembic before starting the app

## Intentional Simplifications

- Google provider behavior is mocked in tests rather than exercised against live Google services
- this lab isolates security flows and does not carry broader workspace/domain logic
