# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/docs/README.md)
- [`docs/concepts/sstable-layout.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/docs/concepts/sstable-layout.md)
- [`docs/concepts/lookup-path.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/docs/concepts/lookup-path.md)
- [`internal/sstable/sstable.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go)
- [`tests/sstable_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/tests/sstable_test.go)
- [`cmd/sstable-format/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/cmd/sstable-format/main.go)
- [`shared/serializer/serializer.go`](/Users/woopinbell/work/book-task-3/database-systems/go/shared/serializer/serializer.go)
- [`shared/fileio/fileio.go`](/Users/woopinbell/work/book-task-3/database-systems/go/shared/fileio/fileio.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format
GOWORK=off go test ./...
GOWORK=off go run ./cmd/sstable-format
GOWORK=off go test ./tests -run TestMalformedFooter -v
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/02-sstable-format/tests (cached)`
- demo:
  - `alpha => 1`
  - `beta => 2`
  - `gamma => <tombstone>`
  - `missing => <missing>`
- malformed footer test:
  - `=== RUN   TestMalformedFooter`
  - `--- PASS: TestMalformedFooter (0.00s)`
  - `PASS`

## Source-grounded claims

- write requires already-sorted input via `validateSorted()`.
- footer stores data and index section lengths as 8 big-endian bytes.
- tombstone sentinel is `math.MaxUint32` in shared serializer.
- lookup reads a fixed 8-byte header first, then re-reads the full record.
- footer mismatch and truncated headers are explicit errors.

## Explicit boundaries

- No compression or checksum
- No block cache
- No manifest or multi-level file management
- No compaction integration
