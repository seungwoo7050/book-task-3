# 01 RPC Framing

length-prefixed TCP framing 위에 간단한 request/response RPC를 올리고, correlation id와 pending call map으로 동시 요청을 처리한다.

- 상태: `verified`
- 구현 언어: `Go 1.26.0`
- 원본: `legacy/distributed-cluster/rpc-network`

## Verification

```bash
cd study/ddia-distributed-systems/01-rpc-framing/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/rpc-framing
```
