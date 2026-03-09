# Verification Report

- Checked date: `2026-03-09`
- Scope: all seven labs plus the capstone
- Reference workflow: [labs-fastapi.yml](/Users/woopinbell/work/web-pong/.github/workflows/labs-fastapi.yml#L1)

## Commands rerun

For each `fastapi/` workspace:

- fresh virtual environment per workspace
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## Result summary

- `labs/A-auth-lab/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes
- `labs/B-federation-security-lab/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes after aligning the PostgreSQL database name with the configured `DATABASE_URL`
- `labs/C-authorization-lab/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes; schema now auto-bootstraps on app startup for local study runs
- `labs/D-data-api-lab/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes; schema now auto-bootstraps on app startup for local study runs
- `labs/E-async-jobs-lab/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes; API schema now auto-bootstraps on app startup for local study runs
- `labs/F-realtime-lab/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes
- `labs/G-ops-lab/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes
- `capstone/workspace-backend/fastapi`: passed compile, lint, tests, smoke, and Compose live/ready probes; schema now auto-bootstraps on app startup for local study runs

## What this does and does not prove

- Proven:
  - the documented Python workspaces install and execute
  - the tracked test suites currently pass
  - the local Docker stacks boot and answer health endpoints
- Not proven:
  - cloud deployment on AWS
  - performance characteristics under load
  - security review beyond the behaviors covered by tests
  - long-running operational behavior for workers and websocket clients

This is a study repository. The verification target is "runnable and inspectable" rather than "production hardened."
