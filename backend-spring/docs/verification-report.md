# study2 Verification Report

- Checked date: `2026-03-09`
- Scope: all seven Spring labs plus both commerce capstones
- Workflow reference: [study2-spring.yml](/Users/woopinbell/work/web-pong/.github/workflows/study2-spring.yml#L1)

## Commands rerun

For every previously tracked `study2/.../spring` workspace:

- `./gradlew spotlessApply test --no-daemon`
- `make test`
- `make lint`
- `make smoke`

Compose probes were also rerun with [tools/compose_probe.sh](/Users/woopinbell/work/web-pong/tools/compose_probe.sh#L1) for every Spring workspace.

For `study2/capstone/commerce-backend-v2/spring`, these commands were rerun explicitly:

- `./gradlew testClasses --no-daemon`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh study2/capstone/commerce-backend-v2/spring 8111`

## Result summary

- `A-auth-lab`: lint, test, smoke, and Compose health probe passed
- `B-federation-security-lab`: lint, test, smoke, and Compose health probe passed
- `C-authorization-lab`: lint, test, smoke, and Compose health probe passed
- `D-data-jpa-lab`: lint, test, smoke, and Compose health probe passed
- `E-event-messaging-lab`: lint, test, smoke, and Compose health probe passed
- `F-cache-concurrency-lab`: lint, test, smoke, and Compose health probe passed after forcing a local in-memory `CacheManager` for test runs
- `G-ops-observability-lab`: lint, test, smoke, and Compose health probe passed
- `commerce-backend`: lint, test, smoke, and Compose health probe passed
- `commerce-backend-v2`: lint, test, smoke, full JUnit suite, Testcontainers messaging test, and Compose health probe passed

## What this proves and what it does not

- Proven:
  - every Spring workspace installs and runs through the documented lint/test/smoke commands
  - the tracked code boots with H2-backed local test settings
  - every tracked Docker stack boots and answers `/api/v1/health/live` and `/api/v1/health/ready`
- Not proven:
  - `make run` was not rerun as a long-lived foreground command for every workspace
  - real Google OAuth console integration
  - long-running production Kafka behavior or AWS deployment
  - production payment provider integration

This is a study repository. The target is runnable and inspectable scaffolding with representative backend patterns, not a production-complete Spring service.
