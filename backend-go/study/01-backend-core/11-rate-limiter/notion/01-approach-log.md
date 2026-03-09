# 접근 과정 — Token Bucket에서 미들웨어까지

## Token Bucket 알고리즘

동작 원리:
1. 버킷에 토큰이 최대 `burst`개까지 들어간다
2. 초당 `rate`개의 토큰이 리필된다
3. 요청이 오면 토큰 한 개를 소비한다
4. 토큰이 없으면 거부한다

**이산적(discrete) 리필이 아니라 연속적(continuous) 리필**을 구현했다. 매 `Allow()` 호출 시 경과 시간을 기반으로 토큰을 계산한다:

```go
elapsed := now.Sub(l.lastTime).Seconds()
l.tokens += elapsed * l.rate
if l.tokens > float64(l.burst) {
    l.tokens = float64(l.burst)
}
```

별도 goroutine으로 주기적 리필을 하지 않는 게 핵심이다. 호출 시점에 계산하므로 goroutine이 필요 없고, 타이머 오버헤드도 없다.

## Limiter 구조체

```go
type Limiter struct {
    mu       sync.Mutex
    rate     float64   // 초당 토큰
    burst    int       // 최대 토큰 (버킷 용량)
    tokens   float64   // 현재 토큰 (float64로 정밀 관리)
    lastTime time.Time // 마지막 계산 시각
}
```

`tokens`를 `float64`로 한 이유: 0.5초 경과 시 0.5 * rate만큼 리필해야 하므로, 정수로는 정밀도가 부족하다.

## Per-Client: ClientLimiter

```go
type ClientLimiter struct {
    mu      sync.Mutex
    clients map[string]*client
    rate    float64
    burst   int
    ttl     time.Duration  // 3분
}
```

각 클라이언트(IP)마다 독립된 `Limiter`를 갖는다. `Allow(ip)` 호출 시:
1. 맵에 해당 IP가 없으면 새 Limiter 생성
2. `lastSeen` 갱신
3. Limiter.Allow() 호출

## Cleanup Goroutine

```go
func (cl *ClientLimiter) cleanup(ctx context.Context) {
    ticker := time.NewTicker(1 * time.Minute)
    defer ticker.Stop()
    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            // 3분 이상 미사용 클라이언트 삭제
        }
    }
}
```

10에서 배운 패턴의 실전 적용:
- `context.Done()`으로 goroutine 종료
- `ticker.Stop()`으로 리소스 정리
- Mutex로 맵 보호

## HTTP Middleware

```go
func RateLimitMiddleware(cl *ClientLimiter) func(http.Handler) http.Handler
```

06에서 확립한 `func(http.Handler) http.Handler` 시그니처를 따른다. 미들웨어 체인에 끼워 넣을 수 있다:

```
recoverPanic → logRequest → rateLimit → enableCORS → router
```

429 응답 시 `Retry-After: 1` 헤더를 설정한다. 클라이언트에게 "1초 후 재시도하라"는 신호.

## IP 추출

```go
func extractIP(r *http.Request) string {
    // X-Forwarded-For → X-Real-IP → RemoteAddr
}
```

리버스 프록시(nginx 등) 뒤에 있으면 `RemoteAddr`이 프록시 IP다. `X-Forwarded-For`를 먼저 확인해야 실제 클라이언트 IP를 얻는다.
