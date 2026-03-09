# E-async-jobs-lab

- Status: `verified`
- Focus: Redis and Celery-backed background jobs with idempotency and outbox handling
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/labs/E-async-jobs-lab/fastapi/README.md#L1)

## Scope

- idempotent notification enqueueing
- outbox persistence and drain endpoint
- Celery worker execution
- retry-aware state transitions

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` passes live/ready probes for API, PostgreSQL, Redis, and worker boot
- local schema is auto-created on app startup for study runs

## Intentional Simplifications

- the worker path is verified with eager-mode tests rather than distributed load testing
- notifications are intentionally generic instead of tied to a product domain
