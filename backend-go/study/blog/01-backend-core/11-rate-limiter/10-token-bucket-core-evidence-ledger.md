# 11 Rate Limiter Evidence Ledger

## 10 token-bucket-core

- 시간 표지: 1단계: 프로젝트 초기화 -> 2단계: 패키지 구조 -> 3단계: Limiter 구조체 (limiter.go) -> 4단계: Allow() 구현 -> 5단계: ClientLimiter 구현 -> 6단계: cleanup goroutine
- 당시 목표: Token Bucket 알고리즘을 직접 구현해야 한다.
- 변경 단위: `solution/go/limiter.go`, `solution/go/limiter_test.go`
- 처음 가설: rate limiter 자체와 HTTP middleware를 분리해 알고리즘과 네트워크 표면을 따로 읽게 했다.
- 실제 조치: 외부 의존성 없음. Go 1.22+. HTTP 서버가 별도 cmd/로 없는 라이브러리 프로젝트: 패키지 이름: `ratelimiter`. `NewLimiter(rate, burst)` — 버킷을 가득 채운 상태로 시작.

CLI:

```bash
cd study/01-backend-core/11-rate-limiter/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/11-rate-limiter
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/limiter.go`
- 새로 배운 것: token bucket은 burst를 허용하면서 평균 처리율을 제한한다.
- 다음: 다음 글에서는 `20-http-middleware-and-bench.md`에서 이어지는 경계를 다룬다.
