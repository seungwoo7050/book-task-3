# study2

`study2/` is the Java/Spring backend track that runs in parallel with the existing FastAPI labs.

## Layout

- `docs/`: Spring-specific curriculum notes, rules, and local notebook templates
- `labs/`: independent Spring Boot labs
- `capstone/`: integrated commerce backend

## Curriculum

- `labs/A-auth-lab`
- `labs/B-federation-security-lab`
- `labs/C-authorization-lab`
- `labs/D-data-jpa-lab`
- `labs/E-event-messaging-lab`
- `labs/F-cache-concurrency-lab`
- `labs/G-ops-observability-lab`
- `capstone/commerce-backend`
- `capstone/commerce-backend-v2`

## Fixed stack

- Java 21
- Spring Boot 3.4.x
- Spring MVC, Spring Security, Validation
- Spring Data JPA + Querydsl
- PostgreSQL, Redis, Kafka, Mailpit
- Flyway
- JUnit 5, MockMvc, Testcontainers
- Docker Compose
- GitHub Actions
- AWS ECS/RDS/ElastiCache oriented deployment guidance

## Workspace shape

Each lab and the capstone keep this tracked structure:

```text
README.md
problem/
spring/
docs/
```

Each `spring/` workspace documents and exposes:

- `make run`
- `make lint`
- `make test`
- `make smoke`
- `docker compose up --build`

`commerce-backend/` is the preserved baseline capstone. `commerce-backend-v2/` is the N+1 upgrade intended to read as the stronger junior-application project.

Open [study2/docs/curriculum.md](/Users/woopinbell/work/web-pong/study2/docs/curriculum.md#L1) first, then pick a lab or capstone README.

Current verification notes live in [study2/docs/verification-report.md](/Users/woopinbell/work/web-pong/study2/docs/verification-report.md#L1).

Public-facing status guidance lives in [study2/docs/publication-status.md](/Users/woopinbell/work/web-pong/study2/docs/publication-status.md#L1).
