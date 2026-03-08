# Verification

## Commands

```bash
cd 04-capstone/17-game-store-capstone/go
mkdir -p ./bin
go build -o ./bin/api ./cmd/api
go test ./...
make repro
```

## Result

- 2026-03-08 기준 `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`가 통과했다.
- 2026-03-08 기준 `go test ./...`가 통과했다.
- 2026-03-08 기준 `make repro`가 통과했다.
  - PostgreSQL compose 기동
  - `schema.sql` 적용
  - `make e2e`로 purchase replay, insufficient balance, idempotency conflict, concurrency 시나리오 검증
