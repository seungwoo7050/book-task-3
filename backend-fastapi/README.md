# web-pong

`web-pong` is a backend-only study repository with two parallel tracks:

- `labs/` and `capstone/`: FastAPI track
- `study2/`: Java/Spring track

The old `ft_transcendence` snapshot remains under `legacy/` as loose historical context. The active learning programs live under `labs/`, `capstone/`, and `study2/` and are intentionally decoupled from the legacy tree.

## Repository layout

- `legacy/`: untouched historical reference
- `labs/`: self-contained FastAPI backend labs
- `capstone/`: integrated final backend project
- `docs/`: shared repository rules, verification notes, and local note templates
- `study2/`: Java/Spring backend labs plus a commerce capstone

## Active FastAPI curriculum

- `labs/A-auth-lab`
- `labs/B-federation-security-lab`
- `labs/C-authorization-lab`
- `labs/D-data-api-lab`
- `labs/E-async-jobs-lab`
- `labs/F-realtime-lab`
- `labs/G-ops-lab`
- `capstone/workspace-backend`

Each lab is independently runnable and testable. There is no shared application package between labs. The capstone re-implements and integrates the concepts instead of importing lab code.

## Active Java/Spring curriculum

- `study2/labs/A-auth-lab`
- `study2/labs/B-federation-security-lab`
- `study2/labs/C-authorization-lab`
- `study2/labs/D-data-jpa-lab`
- `study2/labs/E-event-messaging-lab`
- `study2/labs/F-cache-concurrency-lab`
- `study2/labs/G-ops-observability-lab`
- `study2/capstone/commerce-backend`
- `study2/capstone/commerce-backend-v2`

## Fixed stack

- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Redis
- Celery
- pytest
- Docker Compose
- GitHub Actions
- AWS-oriented deployment guidance

## Spring track stack

- Java 21
- Spring Boot 3.4.x
- Spring MVC, Spring Security, Validation
- Spring Data JPA + Querydsl
- PostgreSQL, Redis, Kafka, Mailpit
- Flyway
- JUnit 5, MockMvc, Testcontainers
- Docker Compose
- GitHub Actions
- AWS-oriented deployment guidance

## Conventions

- All HTTP routes are mounted under `/api/v1`.
- Every FastAPI workspace exposes `/health/live` and `/health/ready`.
- Errors use a consistent envelope shape.
- OpenAPI is generated from code.
- Logs are emitted as structured JSON.
- Every workspace documents `make run`, `make lint`, `make test`, and `make smoke`.
- `notion/` directories are local-only and ignored repo-wide. Templates live in `docs/templates/`.

## Verification

- Validation expectations and publication rules: [docs/repo-standards.md](/Users/woopinbell/work/web-pong/docs/repo-standards.md#L1)
- Current verification record: [docs/verification-report.md](/Users/woopinbell/work/web-pong/docs/verification-report.md#L1)
- Local Compose health probe helper: [tools/compose_probe.sh](/Users/woopinbell/work/web-pong/tools/compose_probe.sh#L1)

Start with [docs/labs-curriculum.md](/Users/woopinbell/work/web-pong/docs/labs-curriculum.md#L1) and then open the lab README you want to study.

For the Spring track, start with [study2/README.md](/Users/woopinbell/work/web-pong/study2/README.md#L1).
