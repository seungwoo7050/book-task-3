# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/docs/README.md)
- [`docs/concepts/virtual-nodes.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/virtual-nodes.md)
- [`docs/concepts/rebalance-accounting.md`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/docs/concepts/rebalance-accounting.md)
- [`internal/routing/routing.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing/routing.go)
- [`tests/routing_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/tests/routing_test.go)
- [`cmd/shard-routing/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing/cmd/shard-routing/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/ddia-distributed-systems/projects/03-shard-routing
GOWORK=off go test ./...
GOWORK=off go run ./cmd/shard-routing
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 empty ring, distribution, moved key count, batch grouping을 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/ddia-distributed-systems/projects/03-shard-routing/tests (cached)`
- demo:
  - `alpha -> node-a`
  - `beta -> node-c`
  - `gamma -> node-b`
- extra snippet:
  - `empty  false`
  - `distribution map[node-a:1148 node-b:939 node-c:913]`
  - `moved_after_add 259`
  - `batch map[node-a:[k5] node-b:[k1 k4] node-c:[k2 k3]]`
  - `nodes_after_remove [node-a node-c node-d]`

## Source-grounded claims

- ring placement uses MurmurHash3 on both keys and `node#vindex`.
- lookup wraps to index `0` when target hash is above the last entry.
- moved-key count is computed by diffing assignment maps.
- duplicate add/remove is currently idempotent.

## Explicit boundaries

- No gossip
- No membership epoch
- No data relocation execution
- No replica placement
- No hotspot/rack awareness
