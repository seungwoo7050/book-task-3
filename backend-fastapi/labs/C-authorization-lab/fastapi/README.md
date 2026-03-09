# C-authorization-lab FastAPI

- Status: `verified`
- Problem scope covered: workspace membership, invitations, RBAC, ownership checks, health endpoints
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

- Compose note: schema is initialized automatically on app startup
