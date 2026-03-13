# 09 Cache Migrations Observability — Cache Invalidation And Fallback

`01-backend-core/09-cache-migrations-observability`는 cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다. 이 글에서는 7단계: GetItem — cache-aside 구현 -> 8단계: UpdateItem — invalidation 구현 -> 9단계: 라우트 등록 -> 10단계: withTrace 미들웨어 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- 7단계: GetItem — cache-aside 구현
- 8단계: UpdateItem — invalidation 구현
- 9단계: 라우트 등록
- 10단계: withTrace 미들웨어

## Day 1
### Session 1

- 당시 목표: `X-Trace-ID`를 응답 헤더에 반영해 최소한의 요청 추적 표면을 만들었다.
- 변경 단위: `solution/go/internal/app/app.go`, `solution/go/internal/app/app_test.go`
- 처음 가설: API, migration, metrics를 한 과제에 묶어 “기능 + 운영 표면”을 동시에 읽게 했다.
- 실제 진행: 핵심: DB 조회 중에는 Lock을 잡지 않는다.

CLI:

```bash
cd 01-backend-core/09-cache-migrations-observability/go
go run ./cmd/server
go test ./...
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

- 쓰기 후 invalidation을 빼먹으면 stale data가 남는다.

보조 코드: `solution/go/internal/app/app_test.go`

```go
func newService(t *testing.T) (*Service, func()) {
	t.Helper()
	db, err := OpenInMemory()
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	ctx := context.Background()
	if err := ApplyUpMigration(ctx, db); err != nil {
		t.Fatalf("up migration: %v", err)
	}
	if err := Seed(ctx, db); err != nil {
		t.Fatalf("seed: %v", err)
	}
	return NewService(db, NewTestLogger()), func() { db.Close() }
}

func TestCacheHitMiss(t *testing.T) {
	t.Parallel()
```

왜 이 코드도 같이 봐야 하는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

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

- 다음 글에서는 `30-metrics-tracing-and-verification.md`에서 이어지는 경계를 다룬다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/internal/app/app.go` 같은 결정적인 코드와 `cd 01-backend-core/09-cache-migrations-observability/go` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
