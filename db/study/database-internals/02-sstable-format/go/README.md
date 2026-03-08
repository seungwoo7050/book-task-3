# Go Implementation

## Scope

- immutable SSTable write
- footer metadata parse
- in-memory sparse key index for point lookup
- tombstone-preserving record round-trip

## Commands

```bash
go test ./...
go run ./cmd/sstable-format
```

## Status

- 상태: `verified`
- known gaps: flush orchestration과 multi-table search는 `03-mini-lsm-store` 범위다.

