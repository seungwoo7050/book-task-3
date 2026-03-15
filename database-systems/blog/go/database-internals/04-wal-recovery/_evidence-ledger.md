# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/docs/README.md)
- [`docs/concepts/wal-record-format.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/docs/concepts/wal-record-format.md)
- [`docs/concepts/recovery-policy.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/docs/concepts/recovery-policy.md)
- [`internal/wal/wal.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/internal/wal/wal.go)
- [`internal/store/store.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/internal/store/store.go)
- [`tests/wal_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/tests/wal_test.go)
- [`cmd/wal-recovery/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/cmd/wal-recovery/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery
GOWORK=off go test ./...
GOWORK=off go run ./cmd/wal-recovery
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 internal/store와 internal/wal을 직접 호출
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/04-wal-recovery/tests (cached)`
- demo:
  - `name => Alice`
  - `city => Seoul`
  - `missing => <missing>`
- extra snippet:
  - `recovered_records 3 put delete beta`
  - `alpha_tombstone_after_reopen true`
  - `beta_after_reopen 2`
  - `wal_size_after_flush 0 sstables 1`

## Source-grounded claims

- store writes to WAL before mutating memtable.
- WAL record header is 13 bytes before key/value payload.
- replay stops at truncated header, truncated payload, or CRC mismatch.
- force flush closes, removes, and recreates `active.wal`.

## Explicit boundaries

- No group commit
- No fsync batching policy analysis
- No multi-writer coordination
- No distributed recovery
- No segmented WAL retention
