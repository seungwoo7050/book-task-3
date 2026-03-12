# Verification

## Commands

```bash
cd 03-platform-engineering/14-cockroach-tx
make -C problem build
make -C problem test

cd 03-platform-engineering/14-cockroach-tx/solution/go
make repro
```

## Result

- 2026-03-08 기준 `make -C problem build`가 통과했다.
- 2026-03-08 기준 `make -C problem test`가 통과했다.
- 2026-03-08 기준 `cd solution/go && make repro`가 통과했다.
  - CockroachDB single-node compose 기동
  - `schema.sql` 적용
  - `POST /api/purchase` HTTP 경로의 DB-backed e2e replay 검증
