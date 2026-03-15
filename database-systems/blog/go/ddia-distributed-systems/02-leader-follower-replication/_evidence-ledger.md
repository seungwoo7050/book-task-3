# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/docs/README.md)
- [`docs/concepts/log-shipping.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/log-shipping.md)
- [`docs/concepts/idempotent-follower.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/docs/concepts/idempotent-follower.md)
- [`internal/replication/replication.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/internal/replication/replication.go)
- [`tests/replication_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/tests/replication_test.go)
- [`cmd/replication/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication/cmd/replication/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/02-leader-follower-replication
GOWORK=off go test ./...
GOWORK=off go run ./cmd/replication
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 initial sync, duplicate replay, incremental delete/overwrite를 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/ddia-distributed-systems/projects/02-leader-follower-replication/tests (cached)`
- demo:
  - `alpha deleted`
  - `beta=2 watermark=2`
- extra snippet:
  - `initial_apply 2 1`
  - `duplicate_apply 0 1`
  - `incremental_apply 2 3`
  - `a_deleted true`
  - `b_value 3`

## Source-grounded claims

- sequential offsets are assigned from `len(log.entries)`.
- follower fetch start is always `watermark + 1`.
- duplicate replay is ignored by offset comparison alone.
- delete is replicated as an ordinary log entry.

## Explicit boundaries

- No leader election
- No quorum
- No log truncation/snapshot install
- No partition handling
- No lag metric
