# 17 Game Store Capstone

## Status

`verified`

## Legacy source

- legacy/04-platform-capstone/09-game-store-capstone (`legacy/04-platform-capstone/09-game-store-capstone/README.md`, not included in this public repo)

## Problem scope

- HTTP API
- transaction, idempotency, optimistic locking
- outbox relay
- rate limiting과 운영 기본 요소

## Build

```bash
cd go
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
```

## Test

```bash
cd go
go test ./...
```

## Verification

- `cd go && mkdir -p ./bin && go build -o ./bin/api ./cmd/api`
- `go test ./...`
- `cd go && make repro`
