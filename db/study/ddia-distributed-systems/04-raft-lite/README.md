# 04 Raft Lite

Raft의 전체 production 기능이 아니라, leader election, vote rule, AppendEntries consistency, majority commit, higher-term step-down이 드러나는 작은 동기 시뮬레이터를 구현한다.

- 상태: `verified`
- 구현 언어: `Go 1.26.0`
- 원본: `legacy/distributed-cluster/consensus`

## Verification

```bash
cd study/ddia-distributed-systems/04-raft-lite/go
GOWORK=off go test ./...
GOWORK=off go run ./cmd/raft-lite
```
