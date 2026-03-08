# 05 Clustered KV Capstone

정적 shard topology와 정적 leader 배치를 가진 작은 clustered KV store를 구현해서, shard routing, leader-follower replication, disk-backed node store를 한 흐름으로 연결한다.

- 상태: `verified`
- 구현 언어: `Go 1.26.0`
- 원본: 신규 추가
- 목적: 레거시 프로젝트셋에 없던 통합 브리지 제공

## Verification

```bash
cd study/ddia-distributed-systems/05-clustered-kv-capstone/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/clustered-kv
```
