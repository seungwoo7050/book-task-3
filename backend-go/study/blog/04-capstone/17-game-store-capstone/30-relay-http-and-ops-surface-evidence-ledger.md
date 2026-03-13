# 17 Game Store Capstone Evidence Ledger

## 30 relay-http-and-ops-surface

- 시간 표지: 9단계: httpapi 구현 -> 10단계: relay 구현 -> 11단계: cmd/api 진입점
- 당시 목표: 문제 정의와 답안 요약, docs/notion을 분리해 제출 가능한 공개 표면을 정리한다.
- 변경 단위: `solution/go/internal/httpapi/handler.go`, `solution/go/internal/relay/relay.go`
- 처음 가설: OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 실제 조치: 4개 엔드포인트 + loggingMiddleware + rateLimitMiddleware. `decoder.DisallowUnknownFields()` 적용. 에러 → HTTP 상태 코드 매핑. `OutboxStore` + `Publisher` 인터페이스. `Relay.PollOnce` 공개 메서드 (테스트용). API + Relay를 같은 프로세스에서 실행 (별도 고루틴). Graceful shutdown: SIGTERM → Relay 중지 → HTTP 서버 Shutdown.

CLI:

```bash
go test ./internal/relay/ -v

# 로컬 실행
make run
# 또는: go run ./cmd/api

# 빌드
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/internal/httpapi/handler.go`
- 새로 배운 것: e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.
- 다음: 다음 글에서는 `40-repro-and-e2e-hardening.md`에서 이어지는 경계를 다룬다.
