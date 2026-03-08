# Go Implementation

## Scope

- O(1) LRU cache
- page fetch and pin/unpin
- dirty tracking and write-back

## Commands

```bash
go test ./...
go run ./cmd/buffer-pool
```

## Status

- 상태: `verified`
- known gaps: page replacement policy는 LRU만 다루며 clock/2Q는 포함하지 않는다.

