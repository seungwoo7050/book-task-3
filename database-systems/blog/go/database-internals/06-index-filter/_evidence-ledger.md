# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/docs/README.md)
- [`docs/concepts/bloom-filter-sizing.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/docs/concepts/bloom-filter-sizing.md)
- [`docs/concepts/sparse-index-scan.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/docs/concepts/sparse-index-scan.md)
- [`internal/sstable/sstable.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/sstable/sstable.go)
- [`internal/bloomfilter/bloom_filter.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/bloomfilter/bloom_filter.go)
- [`internal/sparseindex/sparse_index.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/sparseindex/sparse_index.go)
- [`tests/index_filter_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/tests/index_filter_test.go)
- [`cmd/index-filter/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/cmd/index-filter/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter
rm -rf .demo-data
GOWORK=off go test ./...
rm -rf .demo-data
GOWORK=off go run ./cmd/index-filter
rm -rf .demo-data
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 miss path, hit path, footer metadata를 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/06-index-filter/tests (cached)`
- demo:
  - `durian=gold bytes_read=74`
- extra snippet:
  - `miss false true true 0`
  - `hit true gold 74 0 74`
  - `footer SIF1 96 112 4`

## Source-grounded claims

- Bloom filter uses MurmurHash3 double hashing, not SHA-based hashing.
- sparse index stores one entry per block boundary.
- footer magic is `SIF1` and footer size is 40 bytes.
- miss path can terminate before any data block read.

## Explicit boundaries

- No learned index
- No adaptive filter
- No cache integration
- No range scan optimization
