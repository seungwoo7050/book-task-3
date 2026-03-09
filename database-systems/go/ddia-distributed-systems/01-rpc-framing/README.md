# 01 RPC Framing

## Summary

length-prefixed TCP framing 위에 간단한 request/response RPC를 올리고, correlation id와 pending call map으로 동시 요청을 처리한다.

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/ddia-distributed-systems/01-rpc-framing
GOWORK=off go test ./...
GOWORK=off go run ./cmd/rpc-framing
```
