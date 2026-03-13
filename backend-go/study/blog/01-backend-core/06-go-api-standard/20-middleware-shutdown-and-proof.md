# 06 Go API Standard — Middleware Shutdown And Proof

`01-backend-core/06-go-api-standard`는 표준 라이브러리만으로 REST API, middleware, JSON envelope, graceful shutdown을 정리하는 본선 과제다. 이 글에서는 Phase 3: 핸들러와 미들웨어 구현 -> Phase 4: 서버 기동과 graceful shutdown -> Phase 5: 테스트 -> Phase 6: problem 디렉터리와 Makefile 구간을 따라가면서, 어떤 파일과 어떤 명령이 실제 구현 전환점이었는지 복원한다.

## 구현 순서 요약

- Phase 3: 핸들러와 미들웨어 구현
- Phase 4: 서버 기동과 graceful shutdown
- Phase 5: 테스트
- Phase 6: problem 디렉터리와 Makefile

## Day 1
### Session 1

- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `internal/data/movies_test.go`, `cmd/api/handlers_test.go`
- 처음 가설: DB를 의도적으로 제외해 handler/model/middleware 구조와 종료 시퀀스에 집중하게 했다.
- 실제 진행: helpers.go — JSON I/O 헬퍼 `readJSON`: `json.NewDecoder`로 request body 파싱. 크기 제한, 알 수 없는 필드 거부 등 방어 코드 포함. `writeJSON`: `json.Marshal` → `w.Header().Set` → `w.WriteHeader` → `w.Write` 순서. main.go `slog` 로거 생성 → 환경변수에서 설정 로드(`PORT`, `ENV`) → `application` 구조체 조립 → `serve` 메서드 호출.

CLI:

```bash
cd solution/go
go run ./cmd/api
# time=... level=INFO msg="starting server" addr=:4000 env=development

# 다른 터미널에서:
curl http://localhost:4000/v1/healthcheck
curl -X POST http://localhost:4000/v1/movies \
  -d '{"title":"Inception","year":2010,"runtime":148,"genres":["sci-fi"]}'
curl http://localhost:4000/v1/movies/1
curl http://localhost:4000/v1/movies
curl -X PATCH http://localhost:4000/v1/movies/1 -d '{"year":2011}'
curl -X DELETE http://localhost:4000/v1/movies/1

# graceful shutdown 테스트
kill -SIGTERM <PID>
# 또는 Ctrl+C

cd solution/go
go test ./...
go test -v ./cmd/api/
go test -v ./internal/data/
```

검증 신호:

- time=... level=INFO msg="starting server" addr=:4000 env=development
- httptest 기반. 각 엔드포인트의 정상/에러 케이스를 검증.
- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem build`가 통과했다.
- 남은 선택 검증: `healthcheck` 런타임 검증은 legacy 라운드에서 확인됐고, study 라운드에서는 test/build를 우선 기준으로 사용했다.

핵심 코드: `solution/go/cmd/api/middleware.go`

```go
type responseWriter struct {
	http.ResponseWriter
	statusCode    int
	headerWritten bool
}

func (rw *responseWriter) WriteHeader(code int) {
	if !rw.headerWritten {
		rw.statusCode = code
		rw.headerWritten = true
	}
	rw.ResponseWriter.WriteHeader(code)
}
func (app *application) logRequest(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		wrapped := &responseWriter{
```

왜 이 코드가 중요했는가:

이 블록은 요청 수명주기를 감싸는 순서를 고정한다. recovery, logging, auth, CORS는 순서가 틀리면 의미가 달라지기 때문에 이 코드가 글의 축이 된다.

새로 배운 것:

- JSON envelope는 응답 shape를 고정해 클라이언트와 테스트를 단순하게 만든다.

보조 코드: `solution/go/cmd/api/handlers_test.go`

```go
func newTestApp() *application {
	logger := slog.New(slog.NewTextHandler(&bytes.Buffer{}, nil))
	return &application{
		config: config{port: 4000, env: "testing"},
		logger: logger,
		models: data.NewModels(),
	}
}

func TestHealthcheckHandler(t *testing.T) {
	app := newTestApp()

	tests := []struct {
		name       string
		method     string
		path       string
		wantStatus int
		wantBody   string
```

왜 이 코드도 같이 봐야 하는가:

이 테스트나 재현 스크립트는 프로젝트의 공개 표면을 말이 아니라 입력과 결과로 고정한다. 최종 글에서 이 증거를 빼면 구현은 보여도 완료 기준은 흐려진다.

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

- `healthcheck` 런타임 검증은 legacy 라운드에서 확인됐고, study 라운드에서는 test/build를 우선 기준으로 사용했다.

## 마무리

이 글을 따로 떼어 쓴 이유는 결과 요약보다 구현 순서가 먼저 보이게 하기 위해서다. `solution/go/cmd/api/middleware.go` 같은 결정적인 코드와 `cd 01-backend-core/06-go-api-standard` 같은 검증 명령이 같은 글 안에 있어야, 이 프로젝트가 어떤 경계부터 닫았는지 추적할 수 있다.
