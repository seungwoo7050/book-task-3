# 09 Cache Migrations Observability

## Status

`verified`

## Legacy source

- `study`에서 새로 추가한 브리지 과제

## Problem scope

- cache-aside hit/miss
- cache invalidation
- migration up/down
- structured logging
- `/metrics`
- trace id 기본 전파

## Build

```bash
cd go
go run ./cmd/server
```

## Test

```bash
cd go
go test ./...
```

## Verification

- `go run ./cmd/server`
- `go test ./...`

## Known gaps

- 실제 Redis 대신 in-memory cache adapter를 사용한다.

