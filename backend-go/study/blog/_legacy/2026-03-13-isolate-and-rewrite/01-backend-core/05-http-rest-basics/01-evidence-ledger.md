# 05 HTTP REST Basics Evidence Ledger

이 문서는 기존 `blog/` 초안을 입력으로 읽지 않고, 살아 있는 근거만으로 chronology를 복원한 ledger다.

## 근거 묶음

- 프로젝트 요약: 작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다.
- 구현 디렉터리: `solution/go`
- 주요 구현 파일: `solution/go/internal/api/api.go`, `solution/go/internal/api/api_test.go`
- 대표 검증 명령: `cd solution/go && go test -v ./internal/api`, `cd solution/go && go test -run TestListTasksPagination -v ./internal/api`
- 핵심 개념 축: `GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다., 생성 성공은 `201`, 같은 idempotency key 재시도는 `200`으로 분리했다., validation 실패는 `422`로, 잘못된 JSON이나 path parameter는 `400`으로 다루는 편이 읽기 쉽다., pagination은 작은 예제에서도 응답 shape와 query parameter 처리 감각을 만든다.
- chronology 복원 주석: 이 경로의 git 이력은 대체로 큰 source drop과 문서 보강 위주라 세밀한 시각 정보를 주지 못한다. 그래서 chronology는 README, 살아 있는 소스코드, 테스트, 현재 CLI 재실행 결과를 기준으로 Phase 1/2/3 형태로 복원했다.

## Git History Anchor

- `2026-03-08 46051f3 A large commit`
- `2026-03-09 69364e2 docs(notion): backend-go`
- `2026-03-12 0e12fb8 Track 3에 대한 전반적인 개선 완료 (backend go/node/spring, front react )`

## Chronology Ledger

### 1. Phase 1 - Task와 in-memory Server로 리소스 경계를 먼저 고정한다

- 당시 목표: Task와 in-memory Server로 리소스 경계를 먼저 고정한다
- 변경 단위: `solution/go/internal/api/api.go`의 `NewServer`
- 처음 가설: `NewServer` 쪽에서 상태 경계를 먼저 세우면 HTTP layer는 훨씬 단순해질 것이라고 봤다.
- 실제 조치: `solution/go/internal/api/api.go`의 `NewServer`를 기준으로 상태와 저장소 경계를 먼저 고정했다.
- CLI: `cd solution/go && go test -v ./internal/api`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestHealthcheck`였다.
- 핵심 코드 앵커:
- `NewServer`: `solution/go/internal/api/api.go`

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

- 새로 배운 것: `GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다.
- 다음: Routes와 createTask, listTasks handler로 HTTP 표면을 세운다
### 2. Phase 2 - Routes와 createTask, listTasks handler로 HTTP 표면을 세운다

- 당시 목표: Routes와 createTask, listTasks handler로 HTTP 표면을 세운다
- 변경 단위: `solution/go/internal/api/api.go`의 `createTask`
- 처음 가설: `createTask`에 transport 규칙을 모아 두면 validation과 응답 shape를 한곳에서 설명할 수 있다고 판단했다.
- 실제 조치: `solution/go/internal/api/api.go`의 `createTask`를 통해 transport, validation, auth or cache surface를 노출했다.
- CLI: `cd solution/go && go test -run TestListTasksPagination -v ./internal/api`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestListTasksPagination`였다.
- 핵심 코드 앵커:
- `createTask`: `solution/go/internal/api/api.go`

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

- 새로 배운 것: idempotency key 저장을 메모리에 두면 동작은 보이지만 프로세스 재시작에는 약하다.
- 다음: api_test로 validation, idempotency, pagination 계약을 잠근다
### 3. Phase 3 - api_test로 validation, idempotency, pagination 계약을 잠근다

- 당시 목표: api_test로 validation, idempotency, pagination 계약을 잠근다
- 변경 단위: `solution/go/internal/api/api_test.go`의 `TestCreateTaskIdempotency`
- 처음 가설: `TestCreateTaskIdempotency` 같은 테스트가 있어야 handler, auth, cache 계약이 서로 섞이지 않는다고 봤다.
- 실제 조치: `solution/go/internal/api/api_test.go`의 `TestCreateTaskIdempotency`를 중심으로 handler contract와 edge case를 묶어 재검증 루프를 닫았다.
- CLI: `cd solution/go && go test -run TestListTasksPagination -v ./internal/api`
- 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `=== RUN   TestListTasksPagination`였다.
- 핵심 코드 앵커:
- `TestCreateTaskIdempotency`: `solution/go/internal/api/api_test.go`

```go
func TestCreateTaskIdempotency(t *testing.T) {
	t.Parallel()

	server := NewServer()
	body := []byte(`{"title":"write docs"}`)

	req1 := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewReader(body))
	req1.Header.Set("Idempotency-Key", "abc")
	rr1 := httptest.NewRecorder()
```

- 새로 배운 것: page/page_size를 음수나 0으로 넣었을 때 fallback 규칙을 빼먹기 쉽다.
- 다음: 최종 글은 이 세 phase를 같은 순서로 묶어 development log로 다시 쓴다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/05-http-rest-basics && cd solution/go && go test -v ./internal/api)
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

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/05-http-rest-basics && cd solution/go && go test -run TestListTasksPagination -v ./internal/api)
```

```text
=== RUN   TestListTasksPagination
=== PAUSE TestListTasksPagination
=== CONT  TestListTasksPagination
--- PASS: TestListTasksPagination (0.00s)
PASS
ok  	github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics/internal/api	(cached)
```
