# 09 Cache Migrations Observability Evidence Ledger

## 20 cache-invalidation-and-fallback

- 시간 표지: 7단계: GetItem — cache-aside 구현 -> 8단계: UpdateItem — invalidation 구현 -> 9단계: 라우트 등록 -> 10단계: withTrace 미들웨어
- 당시 목표: `X-Trace-ID`를 응답 헤더에 반영해 최소한의 요청 추적 표면을 만들었다.
- 변경 단위: `solution/go/internal/app/app.go`, `solution/go/internal/app/app_test.go`
- 처음 가설: API, migration, metrics를 한 과제에 묶어 “기능 + 운영 표면”을 동시에 읽게 했다.
- 실제 조치: 핵심: DB 조회 중에는 Lock을 잡지 않는다.

CLI:

```bash
cd 01-backend-core/09-cache-migrations-observability/go
go run ./cmd/server
go test ./...
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/internal/app/app.go`
- 새로 배운 것: 쓰기 후 invalidation을 빼먹으면 stale data가 남는다.
- 다음: 다음 글에서는 `30-metrics-tracing-and-verification.md`에서 이어지는 경계를 다룬다.
