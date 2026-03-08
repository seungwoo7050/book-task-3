# 12 gRPC Microservices

## Status

`verified`

## Legacy source

- legacy/02-distributed-system/04-grpc-microservices (`legacy/02-distributed-system/04-grpc-microservices/README.md`, not included in this public repo)

## Problem scope

- protocol buffers
- unary/streaming RPC 감각
- interceptor
- client/server contract-first 구조

## Build

```bash
make -C problem build-server
make -C problem build-client
```

## Test

```bash
make -C problem test
```

## Verification

- `make -C problem build-server`
- `make -C problem build-client`
- `make -C problem test`

## Known gaps

- generated protobuf code workflow는 hand-written shim 기준으로만 정리되어 있다.
