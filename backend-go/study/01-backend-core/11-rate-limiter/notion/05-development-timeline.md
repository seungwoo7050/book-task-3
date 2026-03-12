# 타임라인 — Rate Limiter 개발 전체 과정

## 1단계: 프로젝트 초기화

```bash
cd study/01-backend-core/11-rate-limiter/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/11-rate-limiter
```

외부 의존성 없음. Go 1.22+.

## 2단계: 패키지 구조

HTTP 서버가 별도 cmd/로 없는 라이브러리 프로젝트:

```
solution/go/
├── go.mod
├── limiter.go
├── limiter_test.go
├── middleware.go
└── middleware_test.go
```

패키지 이름: `ratelimiter`.

## 3단계: Limiter 구조체 (limiter.go)

```go
type Limiter struct {
    mu       sync.Mutex
    rate     float64
    burst    int
    tokens   float64
    lastTime time.Time
}
```

`NewLimiter(rate, burst)` — 버킷을 가득 채운 상태로 시작.

## 4단계: Allow() 구현

```go
func (l *Limiter) Allow() bool {
    l.mu.Lock()
    defer l.mu.Unlock()

    now := time.Now()
    elapsed := now.Sub(l.lastTime).Seconds()
    l.lastTime = now

    l.tokens += elapsed * l.rate
    if l.tokens > float64(l.burst) {
        l.tokens = float64(l.burst)
    }

    if l.tokens >= 1.0 {
        l.tokens -= 1.0
        return true
    }
    return false
}
```

## 5단계: ClientLimiter 구현

```go
type client struct {
    limiter  *Limiter
    lastSeen time.Time
}

type ClientLimiter struct {
    mu      sync.Mutex
    clients map[string]*client
    rate    float64
    burst   int
    ttl     time.Duration  // 3분
}
```

`NewClientLimiter(ctx, rate, burst)` — cleanup goroutine 자동 시작.

## 6단계: cleanup goroutine

```go
func (cl *ClientLimiter) cleanup(ctx context.Context) {
    ticker := time.NewTicker(1 * time.Minute)
    defer ticker.Stop()
    for {
        select {
        case <-ctx.Done(): return
        case <-ticker.C:
            // 3분 미활동 클라이언트 삭제
        }
    }
}
```

## 7단계: HTTP Middleware (middleware.go)

```go
func RateLimitMiddleware(cl *ClientLimiter) func(http.Handler) http.Handler
```

- IP 추출: X-Forwarded-For → X-Real-IP → RemoteAddr
- 제한 초과 시: 429 + Retry-After: 1 + JSON 에러 응답

## 8단계: 테스트 (limiter_test.go)

```bash
go test ./...
```

테스트 목록:
- 버스트 내 Allow() → true
- 버스트 초과 Allow() → false
- 시간 경과 후 리필 확인
- ClientLimiter IP별 독립 제한
- cleanup 후 stale 클라이언트 제거 확인

## 9단계: 미들웨어 테스트 (middleware_test.go)

```bash
go test -run TestMiddleware ./...
```

- burst 내 요청 → 200
- burst 초과 → 429 + Retry-After 헤더 검증
- httptest.NewRecorder 사용

## 10단계: 벤치마크

```bash
go test -bench=. ./...
```

Allow() 호출의 ns/op 측정.

## 11단계: Race detector

```bash
go test -race ./...
```

Mutex로 보호된 모든 접근이 안전한지 확인.

## 파일 목록

| 순서 | 파일 | 설명 |
|------|------|------|
| 1 | `go.mod` | 모듈 정의, 외부 의존성 없음 |
| 2 | `limiter.go` | Limiter, ClientLimiter, cleanup goroutine |
| 3 | `limiter_test.go` | 알고리즘 정확성, 스레드 안전성 테스트 |
| 4 | `middleware.go` | RateLimitMiddleware, extractIP |
| 5 | `middleware_test.go` | 429 응답, Retry-After 검증 |
