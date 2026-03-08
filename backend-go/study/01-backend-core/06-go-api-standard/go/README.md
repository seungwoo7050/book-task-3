# Go Implementation

- Scope: `net/http` API, middleware, in-memory movie store
- Build: `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`
- Test: `go test -race ./...`
- Status: `verified`
- Known gaps: DB-backed persistence 없음
