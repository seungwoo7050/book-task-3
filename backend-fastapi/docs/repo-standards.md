# Repository Standards

## Public structure

Each lab and the capstone should expose this tracked structure:

```text
README.md
problem/
fastapi/
docs/
```

Each `fastapi/` workspace should expose:

```text
app/
tests/
alembic/
pyproject.toml
.env.example
Dockerfile
compose.yaml
Makefile
```

## Runtime conventions

- HTTP routes live under `/api/v1`.
- Health endpoints are `/health/live` and `/health/ready`.
- Errors use the envelope `{ "error": { "code": "...", "message": "...", "details": ... } }`.
- Logs should be machine-readable JSON.
- FastAPI should generate OpenAPI from code.

## Verification expectations

Every workspace should document these commands:

- `make run`
- `make lint`
- `make test`
- `make smoke`

The documented commands should work from the corresponding `fastapi/` directory.

Each workspace should be installed into its own virtual environment. These labs intentionally reuse the top-level package name `app/`, so sharing one interpreter across multiple editable installs will create import collisions.

Compose validation should also be possible from the corresponding `fastapi/` directory with:

```bash
docker compose up --build
```

Repository-level automation may use [tools/compose_probe.sh](/Users/woopinbell/work/web-pong/tools/compose_probe.sh#L1) to verify `/api/v1/health/live` and `/api/v1/health/ready` after boot.

## Publication standard

Before treating the repository as publicly presentable, these conditions should be true:

- root and per-lab READMEs explain scope, validation, and intentional simplifications
- commands shown in tracked docs have been rerun recently
- generated local artifacts such as `.env`, caches, and notebooks stay ignored
- tracked docs do not depend on uncommitted `notion/` content
- verification reports distinguish between tested behavior and untested assumptions

## Local note policy

Per-project `notion/` directories are intentionally excluded from version control. When a local notebook is needed, create it next to the project using the templates under `docs/templates/`.
