# 04 Raft Lite

## Summary

Raft의 전체 production 기능이 아니라, leader election, vote rule, AppendEntries consistency, majority commit, higher-term step-down이 드러나는 작은 동기 시뮬레이터를 구현한다.

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/ddia-distributed-systems/04-raft-lite
GOWORK=off go test ./...
GOWORK=off go run ./cmd/raft-lite
```
