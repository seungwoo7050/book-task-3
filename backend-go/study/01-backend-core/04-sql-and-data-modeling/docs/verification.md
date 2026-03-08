# Verification

## Commands

```bash
cd 01-backend-core/04-sql-and-data-modeling/go
go run ./cmd/schemawalk
go test ./...
```

## Result

- 2026-03-07 기준 `go run ./cmd/schemawalk`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./...`가 통과했다.

## Remaining Checks

- 실제 migration binary와 외부 RDBMS 연결은 다음 과제에서 다룬다.

