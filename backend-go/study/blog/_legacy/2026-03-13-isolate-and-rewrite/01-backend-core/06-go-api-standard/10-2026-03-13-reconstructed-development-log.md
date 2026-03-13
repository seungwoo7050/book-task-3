# 06 Go API Standard 재구성 개발 로그

06 Go API Standard는 표준 라이브러리만으로 REST API, middleware, JSON envelope, graceful shutdown을 정리하는 본선 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: MovieStore와 data model로 API 핵심 상태를 먼저 고정한다 - `solution/go/internal/data/movies.go`의 `NewMovieStore`
- Phase 2: handlers, routes, middleware로 표준 라이브러리 HTTP surface를 조립한다 - `solution/go/cmd/api/handlers.go`의 `createMovieHandler`
- Phase 3: handler/store tests와 race 검증으로 공개 계약을 잠근다 - `solution/go/cmd/api/handlers_test.go`의 `TestCreateMovieHandler`

## Phase 1. MovieStore와 data model로 API 핵심 상태를 먼저 고정한다

- 당시 목표: MovieStore와 data model로 API 핵심 상태를 먼저 고정한다
- 변경 단위: `solution/go/internal/data/movies.go`의 `NewMovieStore`
- 처음 가설: `NewMovieStore` 같은 저장소 경계가 먼저 있어야 handler와 middleware가 표준 라이브러리 수준에서 정리된다고 봤다.
- 실제 진행: `solution/go/internal/data/movies.go`의 `NewMovieStore`에서 in-memory data contract를 먼저 세운 뒤 handler와 분리했다.
- CLI: `cd solution/go && go test -v ./cmd/api`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestHealthcheckHandler`였다.

핵심 코드:

```go
func NewMovieStore() *MovieStore {
	s := &MovieStore{
		movies: make(map[int64]*Movie),
	}
	s.nextID.Store(1)
	return s
}
func (s *MovieStore) Insert(movie *Movie) {
	s.mu.Lock()
```

왜 이 코드가 중요했는가: `NewMovieStore`는 `solution/go/internal/data/movies.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: `application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다.
- 다음: handlers, routes, middleware로 표준 라이브러리 HTTP surface를 조립한다
## Phase 2. handlers, routes, middleware로 표준 라이브러리 HTTP surface를 조립한다

- 당시 목표: handlers, routes, middleware로 표준 라이브러리 HTTP surface를 조립한다
- 변경 단위: `solution/go/cmd/api/handlers.go`의 `createMovieHandler`
- 처음 가설: `createMovieHandler` 쪽에 공개 API 규칙을 모으면 framework 없이도 응답 shape를 안정적으로 유지할 수 있다고 판단했다.
- 실제 진행: `solution/go/cmd/api/handlers.go`의 `createMovieHandler`에 JSON envelope, route, middleware 규칙을 모아 공개 HTTP surface를 정리했다.
- CLI: `cd solution/go && go test -race ./...`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/cmd/api	(cached)`였다.

핵심 코드:

```go
}
func (app *application) createMovieHandler(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Title   string   `json:"title"`
		Year    int32    `json:"year"`
		Runtime int32    `json:"runtime"`
		Genres  []string `json:"genres"`
	}

	err := app.readJSON(w, r, &input)
```

왜 이 코드가 중요했는가: `createMovieHandler`는 `solution/go/cmd/api/handlers.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: 표준 라이브러리만 쓰면 학습엔 좋지만 반복 코드가 늘어난다.
- 다음: handler/store tests와 race 검증으로 공개 계약을 잠근다
## Phase 3. handler/store tests와 race 검증으로 공개 계약을 잠근다

- 당시 목표: handler/store tests와 race 검증으로 공개 계약을 잠근다
- 변경 단위: `solution/go/cmd/api/handlers_test.go`의 `TestCreateMovieHandler`
- 처음 가설: `TestCreateMovieHandler`와 race 검증이 같이 있어야 middleware 순서와 store 동시성까지 닫힌다고 봤다.
- 실제 진행: `solution/go/cmd/api/handlers_test.go`의 `TestCreateMovieHandler`와 race test를 같이 돌려 handler, store, middleware 경계가 실제로 유지되는지 확인했다.
- CLI: `cd solution/go && go test -race ./...`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/cmd/api	(cached)`였다.

핵심 코드:

```go
func TestCreateMovieHandler(t *testing.T) {
	app := newTestApp()

	tests := []struct {
		name       string
		body       map[string]any
		wantStatus int
	}{
		{
```

왜 이 코드가 중요했는가: `TestCreateMovieHandler`는 `solution/go/cmd/api/handlers_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

- 새로 배운 것: middleware 체인 순서를 잘못 두면 panic recovery나 로깅이 기대와 다르게 동작할 수 있다.
- 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## CLI 1. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/06-go-api-standard && cd solution/go && go test -v ./cmd/api)
```

```text
=== RUN   TestHealthcheckHandler
=== RUN   TestHealthcheckHandler/valid_healthcheck
--- PASS: TestHealthcheckHandler (0.00s)
    --- PASS: TestHealthcheckHandler/valid_healthcheck (0.00s)
=== RUN   TestCreateMovieHandler
=== RUN   TestCreateMovieHandler/valid_movie
=== RUN   TestCreateMovieHandler/missing_title
=== RUN   TestCreateMovieHandler/year_too_low
=== RUN   TestCreateMovieHandler/negative_runtime
=== RUN   TestCreateMovieHandler/no_genres
=== RUN   TestCreateMovieHandler/empty_body
--- PASS: TestCreateMovieHandler (0.00s)
    --- PASS: TestCreateMovieHandler/valid_movie (0.00s)
    --- PASS: TestCreateMovieHandler/missing_title (0.00s)
    --- PASS: TestCreateMovieHandler/year_too_low (0.00s)
    --- PASS: TestCreateMovieHandler/negative_runtime (0.00s)
    --- PASS: TestCreateMovieHandler/no_genres (0.00s)
    --- PASS: TestCreateMovieHandler/empty_body (0.00s)
=== RUN   TestShowMovieHandler
=== RUN   TestShowMovieHandler/existing_movie
=== RUN   TestShowMovieHandler/non-existing_movie
=== RUN   TestShowMovieHandler/invalid_id
... (12 more lines)
```
## CLI 2. 현재 저장소에서 다시 돌린 검증

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/06-go-api-standard && cd solution/go && go test -race ./...)
```

```text
ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/cmd/api	(cached)
ok  	github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard/internal/data	(cached)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: `application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다., JSON envelope는 응답 shape를 고정해 클라이언트와 테스트를 단순하게 만든다., `recoverPanic`, 요청 로깅, CORS 같은 middleware는 프레임워크 없이도 충분히 조합 가능하다., graceful shutdown은 SIGINT/SIGTERM 이후 새 요청을 막고 기존 요청을 정리하는 흐름이다.
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: 외부 router 없이 JSON envelope, middleware, graceful shutdown까지 표준 라이브러리로 정리한다.
