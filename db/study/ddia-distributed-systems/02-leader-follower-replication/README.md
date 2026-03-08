# 02 Leader-Follower Replication

leader가 append-only mutation log를 만들고 follower가 watermark 이후의 entry만 받아 idempotent하게 적용하는 복제 경로를 구현한다.

- 상태: `verified`
- 구현 언어: `Go 1.26.0`
- 원본: `legacy/distributed-cluster/replication`

## Verification

```bash
cd study/ddia-distributed-systems/02-leader-follower-replication/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/replication
```
