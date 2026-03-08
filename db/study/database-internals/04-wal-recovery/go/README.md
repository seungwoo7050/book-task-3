# Go Implementation

## Scope

- CRC32-protected WAL append
- stop-on-corruption replay
- append-before-apply durable write path
- flush 후 WAL rotation

## Commands

```bash
go test ./...
go run ./cmd/wal-recovery
```

## Status

- 상태: `verified`
- known gaps: background fsync batching과 log archival policy는 다루지 않는다.

