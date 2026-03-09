# FastAPI Backend Labs Curriculum

## Intent

This repository is organized like a lab course rather than a step-by-step migration. Each lab isolates a backend concern that shows up repeatedly in production FastAPI work. The capstone integrates those concerns into one SaaS-style collaboration backend.

`legacy/` is still useful as historical context, but it is not the active project plan and it does not constrain the lab sequence.

## Why labs instead of one long project

- Backend hiring signals are usually attached to specific concerns such as authentication, authorization, data modeling, background work, realtime delivery, and operations.
- Smaller labs are easier to rerun, debug, and rewrite without carrying accidental complexity from earlier experiments.
- The capstone stays meaningful because it recomposes the ideas instead of merely extending a single starter codebase.

## Lab order

1. `A-auth-lab`
2. `B-federation-security-lab`
3. `C-authorization-lab`
4. `D-data-api-lab`
5. `E-async-jobs-lab`
6. `F-realtime-lab`
7. `G-ops-lab`
8. `capstone/workspace-backend`

## Concept map

### A-auth-lab

- Local signup and login
- Argon2 password hashing
- Email verification
- Password reset
- Refresh-token rotation
- Secure cookie auth
- CSRF validation
- Local email testing with Mailpit

### B-federation-security-lab

- Google OAuth
- External identity linking
- TOTP 2FA
- Recovery codes
- Login throttling
- Auth audit events

### C-authorization-lab

- Workspace membership
- Invitations
- RBAC
- Ownership rules
- Permission boundaries

### D-data-api-lab

- SQLAlchemy models and service boundaries
- CRUD for projects, tasks, and comments
- Filtering and sorting
- Pagination
- Soft delete
- Optimistic locking

### E-async-jobs-lab

- Celery task execution
- Redis-backed queue configuration
- Retry policy
- Idempotency keys
- Outbox handoff

### F-realtime-lab

- WebSocket authentication
- Presence heartbeat
- Notification fan-out
- Reconnect behavior
- Redis-backed pub/sub integration points

### G-ops-lab

- Docker multi-stage images
- Compose-based local stacks
- Health and readiness checks
- Structured logs
- Metrics endpoint
- CI workflow expectations
- AWS deployment shape

### Capstone

- Local auth plus Google OAuth
- Workspace RBAC
- Projects, tasks, and comments
- Async notification delivery
- Realtime notifications and presence
- Production-oriented container and CI layout

## Repository rules

- `legacy/` stays untouched unless the user explicitly asks to modify it.
- Labs are self-contained on purpose, even when that repeats boilerplate.
- `notion/` content is local-only and should not be committed. Use the templates in `docs/templates/`.
- Every lab should be understandable from tracked files alone. Local notebooks are optional, never required.

## Verification philosophy

- `make lint`, `make test`, and `make smoke` verify the code path without Docker.
- `docker compose up --build` plus health probes verify that the documented local stack can boot with its declared dependencies.
- Compose validation is intentionally limited to liveness and readiness. These labs are not pretending to be production-ready systems.
- The capstone is the only place where multiple concerns are intentionally composed into one backend.
