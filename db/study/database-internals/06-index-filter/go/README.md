# Go Implementation

- 상태: `verified`
- 범위: Bloom filter, sparse index, filter/index footer를 갖는 SSTable

## Commands

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/index-filter
```

## Package Layout

- `internal/bloomfilter`: hash-derived bit positions와 membership test
- `internal/sparseindex`: block locator
- `internal/sstable`: integrated on-disk layout과 lookup path
