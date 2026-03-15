# 06-go-api-standard-go 문제지

## 왜 중요한가

Go 표준 라이브러리만 사용해 간단한 Movie 리소스용 RESTful JSON API를 설계하고 구현한다.

## 목표

시작 위치의 구현을 완성해 GET /v1/healthcheck와 Movie CRUD API를 제공한다, 모든 응답이 일관된 JSON envelope 구조를 따른다, 입력 검증, pagination, request logging, panic recovery, CORS를 포함한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/01-backend-core/06-go-api-standard/problem/code/main.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/errors.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/handlers.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/helpers.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/main.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/handlers_test.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/internal/data/movies_test.go`
- `../study/01-backend-core/06-go-api-standard/problem/script/evaluate.sh`

## starter code / 입력 계약

- ../study/01-backend-core/06-go-api-standard/problem/code/main.go에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- GET /v1/healthcheck와 Movie CRUD API를 제공한다.
- 모든 응답이 일관된 JSON envelope 구조를 따른다.
- 입력 검증, pagination, request logging, panic recovery, CORS를 포함한다.
- SIGINT/SIGTERM에서 graceful shutdown이 동작한다.
- third-party router 없이 net/http 기반으로 구현한다.

## 제외 범위

- 실제 DB 연동
- ORM
- third-party router

## 성공 체크리스트

- `../study/01-backend-core/06-go-api-standard/problem/code/main.go`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `errorResponse`와 `serverErrorResponse`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `newTestApp`와 `TestHealthcheckHandler`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/01-backend-core/06-go-api-standard/problem/script/evaluate.sh` fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/06-go-api-standard/problem test
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`06-go-api-standard-go_answer.md`](06-go-api-standard-go_answer.md)에서 확인한다.
