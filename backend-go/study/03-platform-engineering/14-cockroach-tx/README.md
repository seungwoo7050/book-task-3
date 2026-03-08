# 14 Cockroach TX

## Status

`verified`

## Legacy source

- legacy/03-platform-engineering/06-cockroach-tx (`legacy/03-platform-engineering/06-cockroach-tx/README.md`, not included in this public repo)

## Problem scope

- idempotency key
- optimistic locking
- transaction retry
- Cockroach-compatible SQL 흐름

## Build

```bash
make -C problem build
```

## Test

```bash
make -C problem test
```

## Verification

- `make -C problem build`
- `make -C problem test`
- `cd go && make repro`
