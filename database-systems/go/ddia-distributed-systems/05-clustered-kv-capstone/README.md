# 05 Clustered KV Capstone

## Summary

정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store를 구현해서, shard routing, leader-follower replication, disk-backed node store를 한 흐름으로 연결한다.

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/ddia-distributed-systems/05-clustered-kv-capstone
GOWORK=off go test ./...
GOWORK=off go run ./cmd/clustered-kv
```
