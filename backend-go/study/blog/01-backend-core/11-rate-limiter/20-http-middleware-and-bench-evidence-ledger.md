# 11 Rate Limiter Evidence Ledger

## 20 http-middleware-and-bench

- 시간 표지: 7단계: HTTP Middleware (middleware.go) -> 8단계: 테스트 (limiter_test.go) -> 9단계: 미들웨어 테스트 (middleware_test.go) -> 10단계: 벤치마크 -> 11단계: Race detector
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/middleware.go`, `solution/go/middleware_test.go`
- 처음 가설: distributed limiter를 제외해 단일 프로세스 제어 흐름과 동기화 문제를 먼저 익히게 했다.
- 실제 조치: IP 추출: X-Forwarded-For → X-Real-IP → RemoteAddr 제한 초과 시: 429 + Retry-After: 1 + JSON 에러 응답 테스트 목록: 버스트 내 Allow() → true 버스트 초과 Allow() → false 시간 경과 후 리필 확인 ClientLimiter IP별 독립 제한 cleanup 후 stale 클라이언트 제거 확인 burst 내 요청 → 200 burst 초과 → 429 + Retry-After 헤더 검증 httptest.NewRecorder 사용 Allow() 호출의 ns/op 측정.

CLI:

```bash
go test ./...

go test -run TestMiddleware ./...
```

- 검증 신호:
- 2026-03-07 기준 `make -C problem test`가 통과했다.
- 2026-03-07 기준 `make -C problem bench`가 통과했다.
- 남은 선택 검증: Redis-backed shared limiter는 이 과제 범위에 포함하지 않았다.
- 핵심 코드 앵커: `solution/go/middleware.go`
- 새로 배운 것: per-client limiter는 같은 서버 안에서 클라이언트 간 간섭을 줄인다.
- 다음: Redis-backed shared limiter는 이 과제 범위에 포함하지 않았다.
