# 06 Go API Standard — Net Http Surface And Store

`01-backend-core/06-go-api-standard`는 표준 라이브러리만으로 REST API, middleware, JSON envelope, graceful shutdown을 정리하는 본선 과제다. 이 글에서는 Phase 1: 프로젝트 뼈대와 구조 결정 -> Phase 2: 데이터 레이어 구현 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 1: 프로젝트 뼈대와 구조 결정
- Phase 2: 데이터 레이어 구현

## Day 1
### Session 1

- 당시 목표: 표준 라이브러리만으로 RESTful JSON API를 설계해야 한다.
- 변경 단위: `cmd/api/`, `internal/data/models.go`, `internal/data/movies.go`
- 처음 가설: 외부 프레임워크를 빼고 표준 라이브러리만 사용해 HTTP 기초를 드러냈다.
- 실제 진행: 디렉터리 구조 생성 05번과 달리 `cmd/api/`에 여러 Go 파일을 두는 구조를 택했다. 같은 `main` 패키지에 속하는 파일들을 역할별로 분리한다. Movie struct 정의 (`internal/data/models.go`) `Movie` struct에 JSON 태그를 포함. `Version` 필드는 낙관적 잠금을 위한 것이지만 이 과제에서는 아직 사용하지 않는다. `Models` struct는 `MovieStore`를 감싸서 의존성 주입 포인트 역할.

CLI:

```bash
mkdir -p 01-backend-core/06-go-api-standard/{solution/go/cmd/api,solution/go/internal/data,docs/concepts,docs/references,problem}

cd 01-backend-core/06-go-api-standard/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/06-go-api-standard
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/internal/data/movies.go`

```go
var ErrRecordNotFound = errors.New("record not found")

type MovieStore struct {
	mu     sync.RWMutex
	movies map[int64]*Movie
	nextID atomic.Int64
}

func NewMovieStore() *MovieStore {
	s := &MovieStore{
		movies: make(map[int64]*Movie),
	}
	s.nextID.Store(1)
	return s
}
func (s *MovieStore) Insert(movie *Movie) {
	s.mu.Lock()
	defer s.mu.Unlock()
```

왜 이 코드가 중요했는가:

이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.

새로 배운 것:

- `application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다.

보조 코드: `solution/go/cmd/api/main.go`

```go
type config struct {
	port int
	env  string
}
type application struct {
	config config
	logger *slog.Logger
	models data.Models
}

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	}))

	cfg := config{
		port: getEnvInt("PORT", 4000),
		env:  getEnvStr("ENV", "development"),
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 01-backend-core/06-go-api-standard
make -C problem test
make -C problem build
```

검증 신호:

- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem build`가 통과했다.

다음:

- 다음 글에서는 `20-middleware-shutdown-and-proof.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/data/movies.go` 같은 결정적인 코드와 `cd 01-backend-core/06-go-api-standard` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
