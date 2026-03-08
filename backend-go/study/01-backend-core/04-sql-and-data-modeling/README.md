# 04 SQL And Data Modeling

## Status

`verified`

## Legacy source

- `study`에서 새로 추가한 브리지 과제

## Problem scope

- schema 설계와 관계 모델링
- PK/FK, unique constraint, index
- join query와 transaction 기초

## Build

```bash
cd go
go run ./cmd/schemawalk
```

## Test

```bash
cd go
go test ./...
```

## Verification

- `go run ./cmd/schemawalk`
- `go test ./...`

## Known gaps

- 실제 migration tool 적용은 `08-sql-store-api`에서 다룬다.

