# 06-go-api-standard-go 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 GET /v1/healthcheck와 Movie CRUD API를 제공한다, 모든 응답이 일관된 JSON envelope 구조를 따른다, 입력 검증, pagination, request logging, panic recovery, CORS를 포함한다를 한 흐름으로 설명하고 검증한다. 핵심은 `errorResponse`와 `serverErrorResponse`, `notFoundResponse` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- GET /v1/healthcheck와 Movie CRUD API를 제공한다.
- 모든 응답이 일관된 JSON envelope 구조를 따른다.
- 입력 검증, pagination, request logging, panic recovery, CORS를 포함한다.
- 첫 진입점은 `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/errors.go`이고, 여기서 `errorResponse`와 `serverErrorResponse` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/errors.go`: `errorResponse`, `serverErrorResponse`, `notFoundResponse`, `badRequestResponse`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/handlers.go`: `healthcheckHandler`, `createMovieHandler`, `showMovieHandler`, `listMoviesHandler`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/helpers.go`: `writeJSON`, `readJSON`, `readIDParam`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/main.go`: `main`, `serve`, `getEnvStr`, `getEnvInt`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/middleware.go`: `WriteHeader`, `logRequest`, `recoverPanic`, `enableCORS`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/06-go-api-standard/problem/code/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/handlers_test.go`: `newTestApp`, `TestHealthcheckHandler`, `TestCreateMovieHandler`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/01-backend-core/06-go-api-standard/solution/go/internal/data/movies_test.go`: `TestMovieStoreInsertAndGet`, `TestMovieStoreGetNotFound`, `TestMovieStoreUpdate`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/01-backend-core/06-go-api-standard/problem/code/main.go`와 `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/errors.go`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `newTestApp` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/06-go-api-standard/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/06-go-api-standard/problem test
```

- `../study/01-backend-core/06-go-api-standard/problem/code/main.go` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `newTestApp`와 `TestHealthcheckHandler`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/06-go-api-standard/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/errors.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/handlers.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/helpers.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/main.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/middleware.go`
- `../study/01-backend-core/06-go-api-standard/problem/code/main.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/cmd/api/handlers_test.go`
- `../study/01-backend-core/06-go-api-standard/solution/go/internal/data/movies_test.go`
- `../study/01-backend-core/06-go-api-standard/problem/script/evaluate.sh`
- `../study/01-backend-core/06-go-api-standard/problem/Makefile`
