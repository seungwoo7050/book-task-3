# Evidence Ledger

## Primary sources

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/problem/README.md)
- [`README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/docs/README.md)
- [`docs/concepts/b-plus-tree-page-splits.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/docs/concepts/b-plus-tree-page-splits.md)
- [`docs/concepts/range-cursor-and-rule-based-planner.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/docs/concepts/range-cursor-and-rule-based-planner.md)
- [`internal/btreeindex/index.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex/index.go)
- [`internal/queryscan/executor.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan/executor.go)
- [`tests/btree_index_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/tests/btree_index_test.go)
- [`tests/query_scan_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/tests/query_scan_test.go)
- [`cmd/btree-index-and-query-scan/main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/cmd/btree-index-and-query-scan/main.go)

## Re-run commands

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan
GOWORK=off go test ./...
GOWORK=off go run ./cmd/btree-index-and-query-scan
```

추가 재실행:

```bash
tmpfile=$(mktemp ./tmpcheck-XXXX.go)
# project root 안에 임시 Go 파일을 만들어 split height, root separator key, duplicate row-id list, planner strategies를 직접 확인
GOWORK=off go run "$tmpfile"
rm -f "$tmpfile"
```

## Observed outputs

- `go test`: `ok   study.local/go/database-internals/projects/08-btree-index-and-query-scan/tests (cached)`
- demo:
  - `point lookup plan: index-point-lookup ...`
  - `range scan plan: index-range-scan ...`
  - `fallback plan: full-scan ...`
- extra snippet:
  - `height_rootkeys 2 [cora erin] [4 99]`
  - `range_keys [ben cora dina erin]`
  - `plan_eq index-point-lookup`
  - `plan_range index-range-scan`
  - `plan_full full-scan`

## Source-grounded claims

- duplicate key lookup returns a row-id list from one leaf entry.
- leaf split promotes the first key of the right sibling.
- range cursor stops when `entry.Key > end`.
- planner decisions are rule-based and depend only on indexed column alignment plus predicate shape (`Exact` vs `Start/End`), not on selectivity or row counts.

## Explicit boundaries

- No delete merge
- No cost-based optimizer
- No wide-range vs narrow-range heuristic
- No MVCC visibility
- No direct buffer-pool/page integration
- No multi-predicate query model beyond one `Column` with `Exact` or `Start/End`
