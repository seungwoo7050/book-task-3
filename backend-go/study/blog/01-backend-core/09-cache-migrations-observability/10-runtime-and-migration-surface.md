# 09 Cache Migrations Observability — Runtime And Migration Surface

`01-backend-core/09-cache-migrations-observability`는 cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다. 이 글에서는 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: 스키마 및 마이그레이션 정의 (app.go) -> 5단계: Seed 함수 -> 6단계: Service 구조체 정의 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 1단계: 프로젝트 초기화
- 2단계: 외부 의존성 설치
- 3단계: 디렉토리 구조 생성
- 4단계: 스키마 및 마이그레이션 정의 (app.go)
- 5단계: Seed 함수
- 6단계: Service 구조체 정의

## Day 1
### Session 1

- 당시 목표: cache-aside hit/miss와 invalidation을 같이 경험해야 한다.
- 변경 단위: `solution/go/internal/app/app.go`, `solution/go/cmd/server/main.go`
- 처음 가설: 운영성 기본기는 인프라 의존도를 낮춘 상태에서 먼저 익히도록 in-memory cache를 사용했다.
- 실제 진행: 08과 동일한 패턴이지만, 08의 `products`와 구분하기 위해 `items` 테이블을 사용. `mu`: 캐시 맵 동시 접근 보호 `metrics`: atomic 카운터로 lock-free 집계

CLI:

```bash
cd study/01-backend-core/09-cache-migrations-observability/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/09-cache-migrations-observability

go get modernc.org/sqlite
```

검증 신호:

- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.

핵심 코드: `solution/go/internal/app/app.go`

```go
type Item struct {
	ID      int64  `json:"id"`
	Name    string `json:"name"`
	Version int    `json:"version"`
}

type Metrics struct {
	cacheHits   atomic.Int64
	cacheMisses atomic.Int64
	writes      atomic.Int64
}

type Service struct {
	db      *sql.DB
	logger  *slog.Logger
	mu      sync.Mutex
	cache   map[int64]Item
	metrics Metrics
```

왜 이 코드가 중요했는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

새로 배운 것:

- cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.

보조 코드: `solution/go/cmd/server/main.go`

```go
func main() {
	db, err := app.OpenInMemory()
	if err != nil {
		log.Fatal(err)
	}
	ctx := context.Background()
	if err := app.ApplyUpMigration(ctx, db); err != nil {
		log.Fatal(err)
	}
	if err := app.Seed(ctx, db); err != nil {
		log.Fatal(err)
	}

	service := app.NewService(db, nil)
	log.Println("listening on :4050")
	log.Fatal(http.ListenAndServe(":4050", service.Routes()))
}
```

왜 이 코드도 같이 봐야 하는가:

이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.

CLI:

```bash
cd 01-backend-core/09-cache-migrations-observability/go
go run ./cmd/server
go test ./...
```

검증 신호:

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 cache hit/miss, invalidation, `/metrics`, `X-Trace-ID`, migration down을 포함한다.

다음:

- 다음 글에서는 `20-cache-invalidation-and-fallback.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/app/app.go` 같은 결정적인 코드와 `cd 01-backend-core/09-cache-migrations-observability/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
