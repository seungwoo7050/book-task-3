# Problem

작은 JSON API를 만들고 상태 코드, validation, pagination, idempotency를 직접 다룬다.

## Requirements

- `GET /v1/healthcheck`
- `POST /v1/tasks`
- `GET /v1/tasks`
- `GET /v1/tasks/{id}`
- `Idempotency-Key` 헤더로 중복 생성 방지

