# 03 Shard Routing

virtual node를 가진 consistent hash ring으로 key를 node에 배치하고, node 추가/제거 시 얼마나 적은 key만 재배치되는지 측정한다.

- 상태: `verified`
- 구현 언어: `Go 1.26.0`
- 원본: `legacy/distributed-cluster/sharding`

## Verification

```bash
cd study/ddia-distributed-systems/03-shard-routing/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/shard-routing
```
