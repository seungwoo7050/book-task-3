# 09-cache-migrations-observability-go 문제지

## 왜 중요한가

상품 조회 API에 cache-aside 패턴을 적용하고, cache invalidation과 기본 관측 지표를 함께 노출한다.

## 목표

시작 위치의 구현을 완성해 migration up/down이 가능해야 한다, GET /v1/items/{id}와 PUT /v1/items/{id}를 제공한다, /metrics를 노출한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-backend-core/09-cache-migrations-observability/solution/go/cmd/server/main.go`
- `../study/01-backend-core/09-cache-migrations-observability/solution/go/internal/app/app.go`
- `../study/01-backend-core/09-cache-migrations-observability/solution/go/internal/app/app_test.go`
- `../study/01-backend-core/09-cache-migrations-observability/solution/go/go.mod`
- `../study/01-backend-core/09-cache-migrations-observability/solution/go/go.sum`

## starter code / 입력 계약

- `../study/01-backend-core/09-cache-migrations-observability/solution/go/cmd/server/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- migration up/down이 가능해야 한다.
- GET /v1/items/{id}와 PUT /v1/items/{id}를 제공한다.
- /metrics를 노출한다.
- X-Trace-ID 응답 헤더를 전달한다.

## 제외 범위

- 실제 Redis adapter
- full tracing stack
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `OpenInMemory`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `newService`와 `TestCacheHitMiss`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/09-cache-migrations-observability/solution/go && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/09-cache-migrations-observability/solution/go && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`09-cache-migrations-observability-go_answer.md`](09-cache-migrations-observability-go_answer.md)에서 확인한다.
