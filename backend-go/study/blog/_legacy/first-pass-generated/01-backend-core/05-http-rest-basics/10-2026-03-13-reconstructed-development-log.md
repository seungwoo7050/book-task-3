# 05 HTTP REST Basics 재구성 개발 로그

05 HTTP REST Basics는 작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다.

이 글은 2026-03-13에 `isolate-and-rewrite` 방식으로 다시 쓴 버전이다. 기존 `study/blog/` 디렉터리가 없어서 격리할 초안은 없었다. 세밀한 shell history가 남아 있지 않아 시간 표지는 `Phase 1/2/3`처럼 재구성했고, 근거는 README, 살아 있는 소스코드, docs, 테스트, 현재 CLI 재실행 결과만 사용했다.

## 구현 순서 요약

- Phase 1: Task와 in-memory Server로 리소스 경계를 먼저 고정한다 - `solution/go/internal/api/api.go`의 `NewServer`
- Phase 2: Routes와 createTask, listTasks handler로 HTTP 표면을 세운다 - `solution/go/internal/api/api.go`의 `createTask`
- Phase 3: api_test로 validation, idempotency, pagination 계약을 잠근다 - `solution/go/internal/api/api_test.go`의 `TestCreateTaskIdempotency`

                ## Phase 1. Task와 in-memory Server로 리소스 경계를 먼저 고정한다

        - 당시 목표: Task와 in-memory Server로 리소스 경계를 먼저 고정한다
        - 변경 단위: `solution/go/internal/api/api.go`의 `NewServer`
        - 처음 가설: `NewServer` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
        - 실제 진행: `solution/go/internal/api/api.go`의 `NewServer`를 기준으로 상태와 저장소 경계를 먼저 고정했다.
        - CLI: `cd solution/go && go test -v ./internal/api`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestHealthcheck`였다.

        핵심 코드:

        ```go
        func NewServer() *Server {
	return &Server{
		nextID:           1,
		idempotentCreate: make(map[string]Task),
	}
}

func (s *Server) Routes() http.Handler {
	mux := http.NewServeMux()
        ```

        왜 이 코드가 중요했는가: `NewServer`는 `solution/go/internal/api/api.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다.
        - 다음: Routes와 createTask, listTasks handler로 HTTP 표면을 세운다
        ## Phase 2. Routes와 createTask, listTasks handler로 HTTP 표면을 세운다

        - 당시 목표: Routes와 createTask, listTasks handler로 HTTP 표면을 세운다
        - 변경 단위: `solution/go/internal/api/api.go`의 `createTask`
        - 처음 가설: `createTask`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
        - 실제 진행: `solution/go/internal/api/api.go`의 `createTask`를 통해 transport, validation, auth or cache surface를 노출했다.
        - CLI: `cd solution/go && go test -run TestListTasksPagination -v ./internal/api`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestListTasksPagination`였다.

        핵심 코드:

        ```go
        func (s *Server) createTask(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Title string `json:"title"`
	}
	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		writeError(w, http.StatusBadRequest, "invalid json")
		return
	}
	if input.Title == "" {
        ```

        왜 이 코드가 중요했는가: `createTask`는 `solution/go/internal/api/api.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: idempotency key 저장을 메모리에 두면 동작은 보이지만 프로세스 재시작에는 약하다.
        - 다음: api_test로 validation, idempotency, pagination 계약을 잠근다
        ## Phase 3. api_test로 validation, idempotency, pagination 계약을 잠근다

        - 당시 목표: api_test로 validation, idempotency, pagination 계약을 잠근다
        - 변경 단위: `solution/go/internal/api/api_test.go`의 `TestCreateTaskIdempotency`
        - 처음 가설: `TestCreateTaskIdempotency` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
        - 실제 진행: `solution/go/internal/api/api_test.go`의 `TestCreateTaskIdempotency`를 중심으로 handler contract와 edge case를 묶어 재검증 루프를 닫았다.
        - CLI: `cd solution/go && go test -run TestListTasksPagination -v ./internal/api`
        - 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestListTasksPagination`였다.

        핵심 코드:

        ```go
        func TestCreateTaskIdempotency(t *testing.T) {
	t.Parallel()

	server := NewServer()
	body := []byte(`{"title":"write docs"}`)

	req1 := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewReader(body))
	req1.Header.Set("Idempotency-Key", "abc")
	rr1 := httptest.NewRecorder()
        ```

        왜 이 코드가 중요했는가: `TestCreateTaskIdempotency`는 `solution/go/internal/api/api_test.go`에서 판단이 실제로 갈린 지점을 보여 준다. 이 줄이 먼저 고정되어야 다음 phase의 공개 surface나 검증 고리가 과도하게 복잡해지지 않는다.

        - 새로 배운 것: page/page_size를 음수나 0으로 넣었을 때 fallback 규칙을 빼먹기 쉽다.
        - 다음: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

                ## CLI 1. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/05-http-rest-basics && cd solution/go && go test -v ./internal/api)
```

```text
=== RUN   TestHealthcheck
=== PAUSE TestHealthcheck
=== RUN   TestCreateTaskValidation
=== PAUSE TestCreateTaskValidation
=== RUN   TestCreateTaskIdempotency
=== PAUSE TestCreateTaskIdempotency
=== RUN   TestListTasksPagination
=== PAUSE TestListTasksPagination
=== RUN   TestShowTaskNotFound
=== PAUSE TestShowTaskNotFound
=== CONT  TestHealthcheck
=== CONT  TestShowTaskNotFound
=== CONT  TestCreateTaskIdempotency
=== CONT  TestListTasksPagination
=== CONT  TestCreateTaskValidation
--- PASS: TestHealthcheck (0.00s)
--- PASS: TestCreateTaskIdempotency (0.00s)
--- PASS: TestShowTaskNotFound (0.00s)
--- PASS: TestCreateTaskValidation (0.00s)
--- PASS: TestListTasksPagination (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics/internal/api	(cached)
```
        ## CLI 2. 현재 저장소에서 다시 돌린 검증

                ```bash
(cd /Users/woopinbell/work/book-task-3/study/01-backend-core/05-http-rest-basics && cd solution/go && go test -run TestListTasksPagination -v ./internal/api)
```

```text
=== RUN   TestListTasksPagination
=== PAUSE TestListTasksPagination
=== CONT  TestListTasksPagination
--- PASS: TestListTasksPagination (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics/internal/api	(cached)
```

## 이번 재작성에서 남은 것

- 이번 글을 지탱한 개념 축: GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다., 생성 성공은 `201`, 같은 idempotency key 재시도는 `200`으로 분리했다., validation 실패는 `422`로, 잘못된 JSON이나 path parameter는 `400`으로 다루는 편이 읽기 쉽다., `pagination은 작은 예제에서도 응답 shape와 query parameter 처리 감각을 만든다.`
- 최신 검증 메모: 현재 저장소에서 다시 실행한 명령은 모두 exit 0으로 끝났다.
- 다음 질문: 가장 작은 task API에서 route, validation, idempotency를 한 서버로 엮는다.
