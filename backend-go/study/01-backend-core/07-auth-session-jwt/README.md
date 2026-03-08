# 07 Auth Session JWT

## Status

`verified`

## Legacy source

- `study`에서 새로 추가한 브리지 과제

## Problem scope

- cookie session
- bearer JWT
- password hashing
- authentication vs authorization
- 401 vs 403 구분

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

- refresh token과 외부 user store는 다루지 않는다.

