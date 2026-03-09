# G-ops-lab FastAPI

- Status: `verified`
- Problem scope covered: health checks, readiness checks, metrics, JSON logging, container-friendly startup
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
