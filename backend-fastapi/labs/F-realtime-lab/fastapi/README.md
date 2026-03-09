# F-realtime-lab FastAPI

- Status: `verified`
- Problem scope covered: websocket auth, presence heartbeat, fan-out delivery, reconnect-friendly endpoints, health endpoints
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
