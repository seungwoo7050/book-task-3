# Go Implementation

## Scope

- active memtable write path
- flush threshold and immutable swap
- newest-first SSTable search
- reopen after persisted flush

## Commands

```bash
go test ./...
go run ./cmd/mini-lsm-store
```

## Status

- 상태: `verified`
- known gaps: WAL, compaction, Bloom Filter integration은 이후 프로젝트 범위다.

