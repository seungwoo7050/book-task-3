# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/docs/README.md)
- [`docs/concepts/skiplist-invariants.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/docs/concepts/skiplist-invariants.md)
- [`internal/skiplist/skiplist.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go)
- [`tests/skiplist_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go)
- [`cmd/skiplist-demo/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist
GOWORK=off go test ./...
GOWORK=off go run ./cmd/skiplist-demo
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/01-memtable-skiplist/tests (cached)`
- demo:
  - `ordered entries:`
  - `- apple => green`
  - `- banana => <tombstone>`
  - `- carrot => orange`
  - `size=3 byteSize=220`

## Source-grounded claims

- level 0 linked list is the materialized ordered scan path.
- delete is implemented as `put(key, nil)`, not physical removal.
- update keeps logical size constant and only adjusts byte delta.
- byte size uses `nodeOverhead = 64` plus key/value lengths as an approximation.
- RNG seed is fixed to `7` for deterministic level generation.

## Explicit boundaries

- No concurrency control
- No benchmark or level-distribution evaluation
- No actual flush path
- No precise heap accounting
