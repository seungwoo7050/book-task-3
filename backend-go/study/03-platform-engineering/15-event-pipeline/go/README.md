# Go Implementation

- Scope: outbox repository, relay, consumer, CLI entrypoints
- Build: `mkdir -p ./bin && go build -o ./bin/relay ./cmd/relay && go build -o ./bin/consumer ./cmd/consumer`
- Test: `go test ./...`
- Runtime verification: `make repro`
- Status: `verified`
