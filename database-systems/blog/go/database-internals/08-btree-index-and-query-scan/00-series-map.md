# 08 BTree Index And Query Scan

## 이 랩의 실제 초점

이 프로젝트는 B+Tree를 구현한다기보다, buffer pool 위 단계에서 "정렬된 key를 어떻게 split하고, split된 leaf를 어떻게 다시 range scan으로 이어 붙이며, planner는 언제 index를 타야 한다고 말할 수 있는가"를 가장 작은 표면으로 보여 준다. duplicate key는 같은 leaf entry 아래 row id list로 묶고, leaf split은 오른쪽 sibling과 separator key를 만들며, range cursor는 linked leaf를 따라 key order를 유지한다. planner는 cost-based optimizer가 아니라 rule-based 구분만 한다.

즉 이 랩의 핵심은 full SQL engine이 아니라, secondary index와 작은 query executor 사이의 가장 좁은 다리를 source-first로 설명하는 데 있다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/problem/README.md), [`index.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex/index.go), [`executor.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan/executor.go), [`btree_index_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/tests/btree_index_test.go), [`query_scan_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/tests/query_scan_test.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- leaf split은 key order와 duplicate key lookup을 어떻게 유지하는가
- linked leaf range cursor는 어디서 시작하고 어디서 멈추는가
- planner는 어떤 규칙으로 index-point, index-range, full-scan을 나누는가
- 이 구현이 일부러 비워 둔 optimizer/transaction concerns는 무엇인가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/08-btree-index-and-query-scan/10-chronology-scope-and-surface.md): 문제 범위, B+Tree/query executor 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/08-btree-index-and-query-scan/20-chronology-core-invariants.md): leaf/internal split, duplicate key row-id list, range cursor, planner rule set을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/08-btree-index-and-query-scan/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 묶어 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/08-btree-index-and-query-scan/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/08-btree-index-and-query-scan/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 B+Tree와 planner를 각각 크게 만들지 않고도, point lookup, linked-leaf range scan, rule-based fallback full scan이 한 그림으로 이어지는 지점을 보여 준다. delete merge, cost-based optimizer, MVCC visibility는 아직 의도적으로 비워 둔다.

planner 쪽을 더 좁게 말하면, 현재 보장은 "single-column predicate shape heuristic"에 가깝다. `Column == indexedColumn`이고 `Exact`가 있으면 point lookup, `Start/End`가 있으면 range scan, 나머지는 full scan이다. row count, selectivity, range 폭, 복합 predicate는 현재 판단식에 들어오지 않는다.
