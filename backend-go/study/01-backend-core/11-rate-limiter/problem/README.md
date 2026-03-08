# Problem: Rate Limiter

## Objective

Design and implement a **Token Bucket** rate limiter and integrate it as
HTTP middleware.

## Part 1: Token Bucket

### Requirements

1. Implement a `Limiter` that uses the Token Bucket algorithm.
2. The bucket has a configurable **capacity** (burst size) and **refill rate**
   (tokens per second).
3. `Allow()` returns `true` if a token is available (and consumes it), or
   `false` if the bucket is empty.
4. Tokens refill continuously based on elapsed time (not discrete intervals).
5. All operations must be thread-safe.

### Interface

```go
type Limiter struct { ... }

func NewLimiter(rate float64, burst int) *Limiter
func (l *Limiter) Allow() bool
```

## Part 2: Per-Client Rate Limiting

### Requirements

1. Implement a `ClientLimiter` that maintains separate `Limiter` instances
   per client (identified by IP address).
2. Stale entries (no activity for > 3 minutes) must be purged by a background
   cleanup goroutine.
3. The cleanup goroutine must respect context cancellation.

### Interface

```go
type ClientLimiter struct { ... }

func NewClientLimiter(ctx context.Context, rate float64, burst int) *ClientLimiter
func (cl *ClientLimiter) Allow(ip string) bool
```

## Part 3: HTTP Middleware

### Requirements

1. Create an `http.Handler` middleware that uses `ClientLimiter` to rate-limit
   requests by IP.
2. If a client exceeds the limit, respond with `429 Too Many Requests` and
   a `Retry-After` header.
3. The middleware must extract the client IP from `r.RemoteAddr` (strip port).

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Algorithm correctness | 30% | Token bucket refills and depletes correctly |
| Thread safety | 25% | No data races under concurrent access |
| Middleware integration | 20% | Proper 429 responses and header |
| Cleanup goroutine | 15% | Stale entries are purged, no goroutine leaks |
| Tests | 10% | Comprehensive test coverage |
