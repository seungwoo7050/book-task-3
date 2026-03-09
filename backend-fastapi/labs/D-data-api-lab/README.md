# D-data-api-lab

- Status: `verified`
- Focus: PostgreSQL-first CRUD API design with SQLAlchemy service boundaries
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/labs/D-data-api-lab/fastapi/README.md#L1)

## Scope

- projects, tasks, and comments
- filtering, sorting, and page-based pagination
- soft delete behavior
- optimistic locking on project updates

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` passes live/ready probes
- local schema is auto-created on app startup for study runs

## Intentional Simplifications

- pagination is page-based rather than cursor-based
- auth is omitted so the lab can stay focused on data boundaries
