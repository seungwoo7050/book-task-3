# 지식 인덱스 — 빠른 참조용

## 코드 구조

```
cmd/api/
  main.go       — 설정, 의존성 조립, 서버 시작
  routes.go     — 라우트 등록, 미들웨어 체인
  handlers.go   — CRUD 핸들러
  helpers.go    — JSON 읽기/쓰기 헬퍼
  errors.go     — 에러 응답 함수들
  middleware.go — 로깅, panic recovery, CORS
internal/data/
  models.go     — Models 래퍼
  movies.go     — MovieStore (thread-safe in-memory)
```

## Middleware 패턴

```go
func (app *application) middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 전처리
        next.ServeHTTP(w, r)
        // 후처리
    })
}

// 체인: 바깥에서 안으로 실행
app.recoverPanic(app.logRequest(app.enableCORS(mux)))
```

## Graceful shutdown

```go
func (app *application) serve(srv *http.Server) error {
    shutdownErr := make(chan error)
    go func() {
        quit := make(chan os.Signal, 1)
        signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
        <-quit
        ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()
        shutdownErr <- srv.Shutdown(ctx)
    }()
    err := srv.ListenAndServe()
    if !errors.Is(err, http.ErrServerClosed) { return err }
    return <-shutdownErr
}
```

## 환경변수 설정

```bash
PORT=4000 ENV=development go run ./cmd/api
PORT=8080 ENV=production go run ./cmd/api
```

## CLI 명령 정리

```bash
# 빌드
cd solution/go
go build -o api ./cmd/api

# 실행
go run ./cmd/api
PORT=8080 go run ./cmd/api

# 테스트
go test ./...
go test -v ./cmd/api/
go test -v ./internal/data/

# Makefile (problem 디렉터리)
make -C problem build
make -C problem test

# curl 테스트
curl http://localhost:4000/v1/healthcheck
curl -X POST http://localhost:4000/v1/movies -d '{"title":"Inception","year":2010,"runtime":148,"genres":["sci-fi"]}'
curl http://localhost:4000/v1/movies/1
curl http://localhost:4000/v1/movies?page=1&page_size=5
curl -X PATCH http://localhost:4000/v1/movies/1 -d '{"year":2011}'
curl -X DELETE http://localhost:4000/v1/movies/1
```
