# study2 Repository Standards

## Public structure

Each Spring lab and the capstone should expose:

```text
README.md
problem/
spring/
docs/
```

Each `spring/` workspace should expose:

```text
src/main/java
src/main/resources
src/test/java
src/test/resources
build.gradle.kts
settings.gradle.kts
gradlew
gradle/wrapper
.env.example
Dockerfile
compose.yaml
Makefile
```

## Runtime conventions

- REST routes live under `/api/v1`.
- Health endpoints are `/api/v1/health/live` and `/api/v1/health/ready`.
- Errors use `ProblemDetail` with `code`, `traceId`, and `errors` extensions.
- Logs are emitted as JSON.
- OpenAPI is generated from code and served through springdoc.

## Verification expectations

Every `spring/` workspace should document these commands:

- `make run`
- `make lint`
- `make test`
- `make smoke`
- `docker compose up --build`

The documented commands should work from the corresponding `spring/` directory.

## Local note policy

Per-project `notion/` directories remain local-only and ignored repo-wide. Reusable templates live under [study2/docs/templates/notion](/Users/woopinbell/work/web-pong/study2/docs/templates/notion#L1).

## Publication standard

Before presenting `study2/` publicly, these conditions should be true:

- the repo is described as a study track or verified scaffold, not a production system
- every tracked command has been rerun recently
- known simplifications are written down in tracked docs
- local-only notes are not required to understand the repository
