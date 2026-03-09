# D-data-api-lab FastAPI

- Status: `verified`
- Problem scope covered: CRUD, pagination, filtering, sorting, soft delete, optimistic locking, health endpoints
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

- Compose note: schema is initialized automatically on app startup
