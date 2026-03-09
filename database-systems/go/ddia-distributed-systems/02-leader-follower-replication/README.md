# 02 Leader-Follower Replication

## Summary

leader가 append-only mutation log를 만들고 follower가 watermark 이후의 entry만 받아 idempotent하게 적용하는 복제 경로를 구현한다.

## Status

- 상태: `verified`
- 구현 언어: `Go 1.26.0`

## Commands

```bash
cd go/ddia-distributed-systems/02-leader-follower-replication
GOWORK=off go test ./...
GOWORK=off go run ./cmd/replication
```
