# 06 Go API Standard

## Status

`verified`

## Legacy source

- legacy/01-foundation/01-go-api-standard (`legacy/01-foundation/01-go-api-standard/README.md`, not included in this public repo)

## Problem scope

- 표준 라이브러리만 사용한 REST API
- JSON envelope, validation, middleware
- graceful shutdown

## Build

```bash
make -C problem build
```

## Test

```bash
make -C problem test
```

## Verification

- `make -C problem test`
- `make -C problem build`

## Known gaps

- 영속 DB는 포함하지 않는다.

