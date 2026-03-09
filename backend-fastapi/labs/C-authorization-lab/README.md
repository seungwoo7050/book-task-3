# C-authorization-lab

- Status: `verified`
- Focus: workspace membership, invitations, RBAC, and ownership rules
- FastAPI workspace: [fastapi/README.md](/Users/woopinbell/work/web-pong/labs/C-authorization-lab/fastapi/README.md#L1)

## Scope

- workspace creation
- invite creation plus accept/decline flow
- owner/admin/member/viewer role boundaries
- ownership-aware document access

## Validation

- `fastapi/` passes `make lint`, `make test`, and `make smoke`
- `fastapi/compose.yaml` passes live/ready probes
- local schema is auto-created on app startup for study runs

## Intentional Simplifications

- actor identity is provided by header instead of a full auth stack
- this lab is about authorization rules, not authentication correctness
