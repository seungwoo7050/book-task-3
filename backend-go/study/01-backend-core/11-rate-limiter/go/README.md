# Go Implementation

- Scope: token bucket, middleware, concurrency-safe limiter
- Build: `go test ./... -bench=.`
- Test: `go test -race ./...`
- Status: `verified`
- Known gaps: Redis-backed distributed limiting 없음

