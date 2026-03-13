# 06 Go API Standard Evidence Ledger

## 20 middleware-shutdown-and-proof

- 시간 표지: Phase 3: 핸들러와 미들웨어 구현 -> Phase 4: 서버 기동과 graceful shutdown -> Phase 5: 테스트 -> Phase 6: problem 디렉터리와 Makefile
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `internal/data/movies_test.go`, `cmd/api/handlers_test.go`
- 처음 가설: DB를 의도적으로 제외해 handler/model/middleware 구조와 종료 시퀀스에 집중하게 했다.
- 실제 조치: helpers.go — JSON I/O 헬퍼 `readJSON`: `json.NewDecoder`로 request body 파싱. 크기 제한, 알 수 없는 필드 거부 등 방어 코드 포함. `writeJSON`: `json.Marshal` → `w.Header().Set` → `w.WriteHeader` → `w.Write` 순서. main.go `slog` 로거 생성 → 환경변수에서 설정 로드(`PORT`, `ENV`) → `application` 구조체 조립 → `serve` 메서드 호출.

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

- 검증 신호:
- time=... level=INFO msg="starting server" addr=:4000 env=development
- httptest 기반. 각 엔드포인트의 정상/에러 케이스를 검증.
- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem build`가 통과했다.
- 남은 선택 검증: `healthcheck` 런타임 검증은 legacy 라운드에서 확인됐고, study 라운드에서는 test/build를 우선 기준으로 사용했다.
- 핵심 코드 앵커: `solution/go/cmd/api/middleware.go`
- 새로 배운 것: JSON envelope는 응답 shape를 고정해 클라이언트와 테스트를 단순하게 만든다.
- 다음: `healthcheck` 런타임 검증은 legacy 라운드에서 확인됐고, study 라운드에서는 test/build를 우선 기준으로 사용했다.
