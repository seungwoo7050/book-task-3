# Problem: Incident Ops Mobile Client

> Status: IN-PROGRESS
> Scope: RN client 완성작 + 공유 계약 유지
> Last Checked: 2026-03-07

## Objective

Build a React Native incident operations client that is strong enough to function as a hiring-facing capstone:
real screen flow, reproducible tests, offline recovery, and replay-safe realtime behavior, all on top of the existing incident-ops domain.

## Mandatory MVP Scope

1. Auth entry with role selection and session restore.
2. Incident feed with cursor pagination and manual refresh.
3. Incident create form with validation.
4. Role-based actions:
   - operator: `ack`, `request-resolution`
   - approver: `approve`, `reject`
5. Audit timeline in incident detail.
6. Persistent outbox with retry count, failed state, and manual retry.
7. WebSocket reconnect replay using `lastEventId`.

## Intentional Reuse

- Keep the existing incident-ops API and shared contracts.
- Keep the existing node-server as the local backend reference.
- Do not add new required HTTP endpoints for v1 of this client project.

## Out of Scope

- Custom native module work
- OTA/update pipeline work
- Push infrastructure
- Multi-tenant backend redesign

## Evaluation

- `make test`
- `make app-build`
- `make app-test`
- `make server-test`
- `make demo-e2e`

This project is considered complete only when all five commands are reproducible and the RN client remains independent from the earlier capstone directory.
