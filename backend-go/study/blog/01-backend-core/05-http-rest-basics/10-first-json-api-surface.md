# 05 HTTP REST Basics — First Json Api Surface

`01-backend-core/05-http-rest-basics`는 작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다. 이 글에서는 Phase 1: 프로젝트 뼈대 -> Phase 2: 핵심 타입과 서버 구조 -> Phase 3: 핸들러 구현 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 1: 프로젝트 뼈대
- Phase 2: 핵심 타입과 서버 구조
- Phase 3: 핸들러 구현

## Day 1
### Session 1

- 당시 목표: HTTP method와 상태 코드를 단순 암기가 아니라 직접 선택해야 한다.
- 변경 단위: `internal/`, `solution/go/internal/api/api.go`, `"GET /v1/healthcheck"`, `"POST /v1/tasks"`, `"GET /v1/tasks"`, `"GET /v1/tasks/{id}"`
- 처음 가설: 저장소 복잡도를 제거해 상태 코드와 요청 검증에 집중하도록 했다.
- 실제 진행: 디렉터리 구조 생성 `internal/` 디렉터리를 처음 사용했다. Go에서 `internal/` 패키지는 같은 모듈 내에서만 import할 수 있다. API 핸들러를 외부에 노출하지 않겠다는 의도다. Task struct 정의 (`solution/go/internal/api/api.go`) `Task` struct에 JSON 태그를 붙임. `ID`, `Title`, `CreatedAt` 세 필드.

CLI:

```bash
mkdir -p 01-backend-core/05-http-rest-basics/{solution/go/cmd/server,solution/go/internal/api,docs/concepts,docs/references,problem}

cd 01-backend-core/05-http-rest-basics/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/internal/api/api.go`

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

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- `GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다.

보조 코드: `solution/go/cmd/server/main.go`

```go
func main() {
	server := api.NewServer()
	log.Println("listening on :4020")
	log.Fatal(http.ListenAndServe(":4020", server.Routes()))
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

- 다음 글에서는 `20-validation-pagination-and-idempotency.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/api/api.go` 같은 결정적인 코드와 `cd 01-backend-core/05-http-rest-basics/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
