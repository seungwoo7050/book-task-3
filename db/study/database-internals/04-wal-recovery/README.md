# 04 WAL Recovery

## Summary

이 프로젝트는 mutation을 MemTable보다 먼저 WAL에 기록하고, crash 후 replay로 상태를 복구하는 durable write path를 다룬다. flush 후에는 기존 WAL을 버리고 새 active WAL로 회전한다.

## Status

- 상태: `verified`
- 구현 언어: Go 1.26.0
- 검증 명령:

```bash
cd study/database-internals/04-wal-recovery/go
go test ./...
go run ./cmd/wal-recovery
```

