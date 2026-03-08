# 08 SQL Store API

## Status

`verified`

## Legacy source

- `study`에서 새로 추가한 브리지 과제

## Problem scope

- `database/sql` 기반 CRUD API
- migration up/down
- repository 계층
- optimistic update
- transaction rollback

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

- 외부 DB 엔진과 connection pool 튜닝은 다루지 않는다.

