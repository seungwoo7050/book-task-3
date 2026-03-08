# Go Implementation

## Scope

- version chain storage
- snapshot visibility
- first-committer-wins conflict detection
- stale-version garbage collection

## Commands

```bash
go test ./...
go run ./cmd/mvcc
```

## Status

- 상태: `verified`
- known gaps: lock manager, predicate conflict, serializable isolation은 포함하지 않는다.

