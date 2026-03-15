# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/docs/README.md)
- [`docs/concepts/election-cycle.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/docs/concepts/election-cycle.md)
- [`docs/concepts/commit-rule.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/docs/concepts/commit-rule.md)
- [`internal/raft/raft.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft/raft.go)
- [`tests/raft_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/tests/raft_test.go)
- [`cmd/raft-lite/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite/cmd/raft-lite/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/04-raft-lite
GOWORK=off go test ./...
GOWORK=off go run ./cmd/raft-lite
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 first leader, multi-entry commit, failover leader term을 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/ddia-distributed-systems/projects/04-raft-lite/tests (cached)`
- demo:
  - `leader=n1 commit=0 log_len=1`
- extra snippet:
  - `first_leader n1 1`
  - `commit_after_repl 1 2`
  - `failover_leader n2 2`

## Source-grounded claims

- election timeout is deterministic per node, not randomized.
- vote granting checks up-to-date log term/index.
- append mismatch truncates follower suffix.
- commit advancement only considers current-term entries.
- higher term responses force step-down.

## Explicit boundaries

- No persistence
- No restart recovery
- No membership change
- No snapshotting
- No real network transport
