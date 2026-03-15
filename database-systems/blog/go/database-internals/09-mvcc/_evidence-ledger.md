# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/docs/README.md)
- [`docs/concepts/snapshot-visibility.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/docs/concepts/snapshot-visibility.md)
- [`docs/concepts/write-conflict.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/docs/concepts/write-conflict.md)
- [`internal/mvcc/mvcc.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/internal/mvcc/mvcc.go)
- [`tests/mvcc_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/tests/mvcc_test.go)
- [`cmd/mvcc/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc/cmd/mvcc/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/09-mvcc
GOWORK=off go test ./...
GOWORK=off go run ./cmd/mvcc
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 snapshot read, conflict abort, GC 뒤 chain 길이를 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/09-mvcc/tests (cached)`
- demo:
  - `t2 sees x=v1`
- extra snippet:
  - `snapshot_read v1`
  - `conflict_error true`
  - `chain_after_conflict 1`
  - `gc_chain_len 1`

## Source-grounded claims

- snapshot is the max committed tx id at begin time.
- read-your-own-write is checked before visible committed versions.
- conflict detection is commit-time first-committer-wins.
- abort removes only the aborted tx's versions from each written key.
- GC keeps recent versions plus at most one older fallback version.

## Explicit boundaries

- No predicate locking
- No phantom control
- No distributed transaction
- No lock table
- No SQL engine integration
