# Verification

## Commands

```bash
cd 01-backend-core/08-sql-store-api/go
go run ./cmd/server
go test ./...
```

## Result

- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 migration up/down, CRUD, optimistic update, rollback 성격의 재고 예약을 포함한다.

## Remaining Checks

- 외부 DB 연결과 connection pool 조정은 다루지 않았다.

