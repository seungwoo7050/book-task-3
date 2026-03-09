# A-auth-lab FastAPI

- Status: `verified`
- Problem scope covered: local signup/login, Argon2 hashing, email verification, password reset, rotating refresh tokens, cookie auth, CSRF, health endpoints
- Build command:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
cp .env.example .env
make run
```

- Lint command:

```bash
make lint
```

- Test command:

```bash
make test
```

- Smoke command:

```bash
make smoke
```

- Docker command:

```bash
docker compose up --build
```

- Current status: runnable lab with tested local auth flows
- Compose note: schema is initialized automatically on app startup, so the local stack is usable immediately after boot
- Known gaps:
  - Email delivery is local-only and uses Mailpit in Compose
  - Tests use SQLite instead of PostgreSQL for speed
  - Federation and 2FA are intentionally deferred to `B-federation-security-lab`
