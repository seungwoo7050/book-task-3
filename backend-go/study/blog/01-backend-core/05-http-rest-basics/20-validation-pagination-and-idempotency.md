# 05 HTTP REST Basics — Validation Pagination And Idempotency

`01-backend-core/05-http-rest-basics`는 작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다. 이 글에서는 Phase 4: CLI 서버 -> Phase 5: 테스트 -> Phase 6: 문서 및 최종 검증 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 4: CLI 서버
- Phase 5: 테스트
- Phase 6: 문서 및 최종 검증

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/cmd/server/main.go`, `solution/go/internal/api/api_test.go`
- 처음 가설: idempotency는 완성형 분산 설계가 아니라 “왜 필요한가”를 보여 주는 최소 형태로 제한했다.
- 실제 진행: main.go 작성 (`solution/go/cmd/server/main.go`) 서버 실행 및 curl 테스트 httptest 기반 테스트 (`solution/go/internal/api/api_test.go`) 테스트 실행

CLI:

```bash
# 터미널 1: 서버 시작
cd solution/go
go run ./cmd/server

# 터미널 2: curl 테스트
curl http://localhost:4020/v1/healthcheck
# {"status":"available"}

curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}'
# {"task":{"id":1,"title":"write docs","created_at":"..."}}

curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}' -H "Idempotency-Key: abc"
# 201 Created (첫 번째)

curl -X POST http://localhost:4020/v1/tasks -d '{"title":"write docs"}' -H "Idempotency-Key: abc"
# 200 OK (재시도)

curl http://localhost:4020/v1/tasks
# {"tasks":[...],"meta":{"page":1,"page_size":20,"total":2}}

curl http://localhost:4020/v1/tasks/1
# {"task":{"id":1,...}}

curl http://localhost:4020/v1/tasks/999
# {"error":{"message":"task not found"}} (404)

cd solution/go
go test ./...
go test -v ./internal/api/
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 서버 실행은 로컬에서 가능한 상태이며 기본 포트는 `:4020`이다.
- 남은 선택 검증: persistence와 인증은 이 과제 범위에 포함하지 않았다.

핵심 코드: `solution/go/internal/api/api_test.go`

```go
func TestHealthcheck(t *testing.T) {
	t.Parallel()

	req := httptest.NewRequest(http.MethodGet, "/v1/healthcheck", nil)
	rr := httptest.NewRecorder()

	NewServer().Routes().ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Fatalf("status = %d, want %d", rr.Code, http.StatusOK)
	}
}

func TestCreateTaskValidation(t *testing.T) {
	t.Parallel()

	req := httptest.NewRequest(http.MethodPost, "/v1/tasks", bytes.NewBufferString(`{"title":""}`))
	rr := httptest.NewRecorder()
```

왜 이 코드가 중요했는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

새로 배운 것:

- 생성 성공은 `201`, 같은 idempotency key 재시도는 `200`으로 분리했다.

보조 코드: `solution/go/internal/api/api.go`

```go
type Task struct {
	ID        int64     `json:"id"`
	Title     string    `json:"title"`
	CreatedAt time.Time `json:"created_at"`
}

type Server struct {
	mu               sync.Mutex
	nextID           int64
	tasks            []Task
	idempotentCreate map[string]Task
}

func NewServer() *Server {
	return &Server{
		nextID:           1,
		idempotentCreate: make(map[string]Task),
	}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 01-backend-core/05-http-rest-basics/go
go run ./cmd/server
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 서버 실행은 로컬에서 가능한 상태이며 기본 포트는 `:4020`이다.

다음:

- persistence와 인증은 이 과제 범위에 포함하지 않았다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/api/api_test.go` 같은 결정적인 코드와 `cd 01-backend-core/05-http-rest-basics/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
