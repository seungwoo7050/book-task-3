# 13 Distributed Log Core

## Status

`verified`

## Legacy source

- legacy/02-distributed-system/05-distributed-log (`legacy/02-distributed-system/05-distributed-log/README.md`, not included in this public repo)

## Problem scope

- append-only store
- mmap index
- segment rotation
- log abstraction

## Build

```bash
cd go
go test ./log/... -bench=.
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

- replication은 study 본선 범위에서 제외했다.

