# 08 BTree Index And Query Scan 시리즈 맵

`08 BTree Index And Query Scan`은 Database Internals 트랙에서 buffer pool 다음에 오는 index 계층이다. 여기서는 split, lookup, range scan, planner가 따로가 아니라 같은 문제를 어떻게 나눠 붙잡는지 순서대로 읽는다.

## 먼저 보고 갈 질문

- split 뒤에도 key 오름차순과 duplicate key lookup이 유지돼야 합니다.
- range predicate가 index column에 걸릴 때 왜 full scan을 피할 수 있는지 설명할 수 있어야 합니다.

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)

## 재검증 명령

```bash
GOWORK=off go test ./...
GOWORK=off go run ./cmd/btree-index-and-query-scan
```

## 이번 시리즈가 근거로 삼은 파일

- `database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex/index.go`
- `database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan/executor.go`
- `database-systems/go/database-internals/projects/08-btree-index-and-query-scan/tests/btree_index_test.go`
- `database-systems/go/database-internals/projects/08-btree-index-and-query-scan/tests/query_scan_test.go`
- `database-systems/go/database-internals/projects/08-btree-index-and-query-scan/README.md`
- `database-systems/go/database-internals/projects/08-btree-index-and-query-scan/problem/README.md`

## 보조 메모

작업 메모가 꼭 필요할 때만 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)를 본다.
