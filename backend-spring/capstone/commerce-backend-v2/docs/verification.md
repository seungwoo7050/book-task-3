# commerce-backend-v2 Verification

- Checked date: `2026-03-09`
- Workspace: [spring/README.md](/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/README.md#L1)

## Commands rerun

- `./gradlew testClasses --no-daemon`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh study2/capstone/commerce-backend-v2/spring 8111`

## What passed

- full JUnit suite including MockMvc tests and a Testcontainers-backed messaging test
- formatting and checkstyle
- smoke tests
- Docker image build and Compose health probe for `/api/v1/health/live` and `/api/v1/health/ready`

## What is still intentionally limited

- Google OAuth remains mocked at the callback contract level
- payment provider integration is mock-only
- AWS deployment remains documented rather than live-provisioned
