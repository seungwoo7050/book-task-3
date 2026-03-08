# 15 Event Pipeline

## Status

`verified`

## Legacy source

- legacy/03-platform-engineering/07-event-pipeline (`legacy/03-platform-engineering/07-event-pipeline/README.md`, not included in this public repo)

## Problem scope

- outbox pattern
- relay process
- idempotent consumer
- at-least-once semantics

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
