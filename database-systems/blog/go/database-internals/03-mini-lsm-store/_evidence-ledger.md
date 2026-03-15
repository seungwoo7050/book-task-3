# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/docs/README.md)
- [`docs/concepts/flush-lifecycle.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/docs/concepts/flush-lifecycle.md)
- [`docs/concepts/read-path.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/docs/concepts/read-path.md)
- [`internal/lsmstore/store.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/internal/lsmstore/store.go)
- [`tests/lsm_store_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/tests/lsm_store_test.go)
- [`cmd/mini-lsm-store/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store/cmd/mini-lsm-store/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store
GOWORK=off go test ./...
GOWORK=off go run ./cmd/mini-lsm-store
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 internal/lsmstore를 직접 호출
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/03-mini-lsm-store/tests (cached)`
- demo:
  - `apple => <tombstone>`
  - `banana => ripe`
  - `missing => <missing>`
- extra snippet:
  - `sstables_after_flush 2 000002.sst`
  - `beta_active_wins 3`
  - `alpha_tombstone true`
  - `reopened_sstables 2 000002.sst`
  - `reopened_beta 3`
  - `reopened_alpha_tombstone true`

## Source-grounded claims

- flush swaps `Memtable` into `ImmutableMemtable` before writing SSTable.
- `SSTables` is maintained newest-first both on flush and on reopen.
- lookup returns tombstone as `found=true, value=nil`, not as missing.
- reopen derives `nextSequence` from `.sst` filenames.

## Explicit boundaries

- No WAL
- No background compaction
- No concurrent flush
- No flush failure rollback
- No range scan or compression
