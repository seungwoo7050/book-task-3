# 05 HTTP REST Basics Series Map

`01-backend-core/05-http-rest-basics`는 작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다.

## 이 시리즈가 복원하는 것

- 시작점: HTTP method와 상태 코드를 단순 암기가 아니라 직접 선택해야 한다.
- 구현 축: `GET /v1/healthcheck`, `POST /v1/tasks`, 조회 API를 포함한 작은 JSON API를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `go test ./...`가 통과했다.
- 글 수: 2편

## 읽는 순서

- [10-first-json-api-surface.md](10-first-json-api-surface.md)
- [20-validation-pagination-and-idempotency.md](20-validation-pagination-and-idempotency.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
