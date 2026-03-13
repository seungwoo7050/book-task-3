# Evidence Ledger

| phase | focus | evidence |
| --- | --- | --- |
| 1 | split과 planner 경계를 다시 좁힌다 | `README.md`, `problem/README.md` |
| 2 | split / separator / linked leaf invariant를 고정한다 | `internal/btreeindex/index.go`, `tests/btree_index_test.go` |
| 3 | planner가 index와 full scan을 올바르게 고르는지 확인한다 | `internal/queryscan/executor.go`, `tests/query_scan_test.go`, `cmd/btree-index-and-query-scan/main.go` |
