# Go Implementation

- 상태: `verified`
- 범위: single-step `L0 -> L1` compaction, manifest persistence, SSTable read/write

## Commands

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/leveled-compaction
```

## Package Layout

- `internal/sstable`: compacted output를 위한 최소 SSTable
- `internal/compaction`: merge, level metadata, manifest 관리
- `tests`: merge semantics와 file lifecycle 검증
