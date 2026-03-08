# 10 Concurrency Patterns

## Status

`verified`

## Legacy source

- legacy/01-foundation/02-concurrency-patterns (`legacy/01-foundation/02-concurrency-patterns/README.md`, not included in this public repo)

## Problem scope

- worker pool
- pipeline
- context cancellation
- benchmark와 goroutine 종료 경로

## Build

```bash
make -C problem run-workerpool
make -C problem run-pipeline
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

- 실서비스 backpressure 정책은 다루지 않는다.

