# 05-http-rest-basics-go 문제지

## 왜 중요한가

작은 JSON API를 만들고 상태 코드, validation, pagination, idempotency를 직접 다룬다.

## 목표

시작 위치의 구현을 완성해 GET /v1/healthcheck, POST /v1/tasks, GET /v1/tasks를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-backend-core/05-http-rest-basics/solution/go/cmd/server/main.go`
- `../study/01-backend-core/05-http-rest-basics/solution/go/internal/api/api.go`
- `../study/01-backend-core/05-http-rest-basics/solution/go/internal/api/api_test.go`
- `../study/01-backend-core/05-http-rest-basics/solution/go/go.mod`

## starter code / 입력 계약

- `../study/01-backend-core/05-http-rest-basics/solution/go/cmd/server/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- GET /v1/healthcheck
- POST /v1/tasks
- GET /v1/tasks
- GET /v1/tasks/{id}
- Idempotency-Key 헤더로 중복 생성 방지

## 제외 범위

- DB persistence
- 인증
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `NewServer`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestHealthcheck`와 `TestCreateTaskValidation`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/05-http-rest-basics/solution/go && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/05-http-rest-basics/solution/go && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`05-http-rest-basics-go_answer.md`](05-http-rest-basics-go_answer.md)에서 확인한다.
