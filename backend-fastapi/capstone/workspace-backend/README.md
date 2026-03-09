# workspace-backend

- Status: `verified`
- Focus: capstone integration of auth, workspace RBAC, projects/tasks/comments, queued notifications, and realtime delivery
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/capstone/workspace-backend/fastapi/README.md#L1)

## Scope

- local signup/login plus Google-style federated login
- workspace membership and invite flow
- projects, tasks, and comments
- queued notifications plus websocket delivery
- backend-only capstone composition of the earlier labs

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` passes live/ready probes
- local schema is auto-created on app startup for study runs

## Intentional Simplifications

- the capstone re-implements concepts instead of importing lab packages
- frontend rendering, asset serving, and cloud provisioning are intentionally excluded
