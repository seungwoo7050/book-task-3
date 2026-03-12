# 문제 정의

작은 JSON API를 만들고 상태 코드, validation, pagination, idempotency를 직접 다룬다.

## 성공 기준

- `GET /v1/healthcheck`
- `POST /v1/tasks`
- `GET /v1/tasks`
- `GET /v1/tasks/{id}`
- `Idempotency-Key` 헤더로 중복 생성 방지

## 제공 자료와 출처

- `study`에서 새로 설계한 브리지 과제다.
- 이 문서가 공개용 canonical 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- DB persistence
- 인증
