# 타임라인 — 캐시·관측성 개발 전체 과정

## 1단계: 프로젝트 초기화

```bash
cd study/01-backend-core/09-cache-migrations-observability/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/09-cache-migrations-observability
```

## 2단계: 외부 의존성 설치

```bash
go get modernc.org/sqlite
```

## 3단계: 디렉토리 구조 생성

```bash
mkdir -p internal/app
mkdir -p cmd/server
```

```
go/
├── go.mod
├── cmd/
│   └── server/
│       └── main.go
└── internal/
    └── app/
        ├── app.go
        └── app_test.go
```

## 4단계: 스키마 및 마이그레이션 정의 (app.go)

```go
const upMigration = `
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1
);`

const downMigration = `DROP TABLE IF EXISTS items;`
```

08과 동일한 패턴이지만, 08의 `products`와 구분하기 위해 `items` 테이블을 사용.

## 5단계: Seed 함수

```go
func Seed(ctx context.Context, db *sql.DB) error {
    _, err := db.ExecContext(ctx, `
INSERT INTO items(id, name, version) VALUES
    (1, 'starter-sword', 1),
    (2, 'healing-potion', 1)`)
    return err
}
```

## 6단계: Service 구조체 정의

```go
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
}
```

- `mu`: 캐시 맵 동시 접근 보호
- `metrics`: atomic 카운터로 lock-free 집계

## 7단계: GetItem — cache-aside 구현

```go
func (s *Service) GetItem(ctx context.Context, id int64) (Item, error) {
    // 1. Lock → cache 확인 → Unlock
    // 2. miss면: DB 조회
    // 3. Lock → cache 저장 → Unlock
    // 4. 반환
}
```

핵심: DB 조회 중에는 Lock을 잡지 않는다.

## 8단계: UpdateItem — invalidation 구현

```go
func (s *Service) UpdateItem(ctx context.Context, item Item) error {
    // 1. DB UPDATE
    // 2. Lock → delete(cache, id) → Unlock
    // 3. writes 카운터 증가
}
```

## 9단계: 라우트 등록

```go
mux.HandleFunc("GET /v1/items/{id}", s.withTrace(s.showItem))
mux.HandleFunc("PUT /v1/items/{id}", s.withTrace(s.updateItem))
mux.HandleFunc("GET /metrics", s.metricsHandler)
```

## 10단계: withTrace 미들웨어

```go
func (s *Service) withTrace(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        traceID := r.Header.Get("X-Trace-ID")
        if traceID == "" {
            traceID = fmt.Sprintf("trace-%d", rand.Int63())
        }
        w.Header().Set("X-Trace-ID", traceID)
        s.logger.Info("request", "trace_id", traceID, "method", r.Method, "path", r.URL.Path)
        next(w, r)
    }
}
```

## 11단계: /metrics 핸들러

```go
func (s *Service) metricsHandler(w http.ResponseWriter, _ *http.Request) {
    w.Header().Set("Content-Type", "text/plain; version=0.0.4")
    fmt.Fprintf(w, "cache_hits_total %d\ncache_misses_total %d\nwrites_total %d\n",
        s.metrics.cacheHits.Load(),
        s.metrics.cacheMisses.Load(),
        s.metrics.writes.Load())
}
```

## 12단계: main.go 작성

```go
db, _ := app.OpenInMemory()
app.ApplyUpMigration(ctx, db)
app.Seed(ctx, db)
service := app.NewService(db, nil)
log.Println("listening on :4050")
http.ListenAndServe(":4050", service.Routes())
```

포트 4050 사용.

## 13단계: 테스트 작성

```bash
go test ./internal/app/...
```

- `TestCacheHitMiss` — 첫 조회 miss, 두 번째 hit 확인
- `TestInvalidationOnUpdate` — update 후 다시 조회하면 miss (cacheMisses = 2)
- `TestMetricsEndpoint` — /metrics 응답에 `cache_hits_total` 존재 확인
- `TestTraceHeader` — X-Trace-ID 요청 헤더가 응답에 그대로 전파됨
- `TestUpdateEndpoint` — PUT 후 200 응답

## 14단계: 실행 및 검증

```bash
go run ./cmd/server
```

### 아이템 조회 (first = miss)

```bash
curl http://localhost:4050/v1/items/1
```

### 다시 조회 (cache hit)

```bash
curl http://localhost:4050/v1/items/1
```

### 메트릭 확인

```bash
curl http://localhost:4050/metrics
# cache_hits_total 1
# cache_misses_total 1
# writes_total 0
```

### 아이템 수정 (invalidation)

```bash
curl -X PUT http://localhost:4050/v1/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"starter-axe"}'
```

### Trace ID 전파 확인

```bash
curl -v -H "X-Trace-ID: my-trace-123" http://localhost:4050/v1/items/1
# 응답의 X-Trace-ID: my-trace-123
```

## 파일 목록

| 순서 | 파일 | 설명 |
|------|------|------|
| 1 | `go.mod` | 모듈 정의, modernc.org/sqlite 의존성 |
| 2 | `internal/app/app.go` | Service, 캐시, 메트릭, 핸들러, 미들웨어 |
| 3 | `internal/app/app_test.go` | hit/miss, invalidation, metrics, trace 테스트 |
| 4 | `cmd/server/main.go` | 엔트리포인트, :4050 |
