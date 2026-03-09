# B-federation-security-lab FastAPI

- Status: `verified`
- Problem scope covered: Google OIDC login, identity linking, rotating refresh tokens, CSRF, TOTP 2FA, recovery codes, auth audit logs, health endpoints
- Build command:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
cp .env.example .env
make run
```

- Commands:

```bash
make lint
make test
make smoke
docker compose up --build
```

- Compose note: the API container applies `alembic upgrade head` before starting FastAPI
- Known gaps:
  - Google provider behavior is mocked in tests
  - this lab focuses on auth security, not broader product domain modeling
