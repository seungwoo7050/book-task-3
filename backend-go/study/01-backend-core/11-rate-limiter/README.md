# 11 Rate Limiter

## Status

`verified`

## Legacy source

- legacy/01-foundation/03-rate-limiter (`legacy/01-foundation/03-rate-limiter/README.md`, not included in this public repo)

## Problem scope

- token bucket
- per-client isolation
- middleware integration
- stale client cleanup

## Build

```bash
cd go
go test ./... -bench=.
```

## Test

```bash
make -C problem test
make -C problem bench
```

## Verification

- `make -C problem test`
- `make -C problem bench`

## Known gaps

- 분산 환경에서의 shared limiter는 다루지 않는다.

