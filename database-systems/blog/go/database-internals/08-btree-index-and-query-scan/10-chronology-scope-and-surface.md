# Scope, Split Surface, And Query Plans

## 1. 문제 범위는 B+Tree 전체가 아니라 split, cursor, planner의 최소 집합이다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/problem/README.md)는 leaf insert ordering, leaf split과 separator key, duplicate key row-id list, linked-leaf range scan, 그리고 indexed equality/range vs non-indexed predicate planner를 요구한다. delete merge, cost-based optimizer, join, transaction visibility는 뺀다.

즉 이 랩은 query engine 전체를 다루는 단계가 아니라, index를 만들고 나서 "이제 query surface가 무엇을 달리 말할 수 있게 되는가"를 작은 범위로 고정하는 단계다.

## 2. 코드 표면은 index와 executor 두 층으로 나뉜다

핵심 구현은 두 파일에 나뉜다.

- [`index.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex/index.go): insert, split, lookup, range cursor
- [`executor.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan/executor.go): row store, planner, point/range/full scan execution

이 분리 덕분에 B+Tree 자체의 ordering semantics와 planner의 "왜 지금 index를 탈 수 있는가" 설명을 따로 읽을 수 있다.

## 3. demo는 세 가지 planner 전략을 한 번에 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan
GOWORK=off go run ./cmd/btree-index-and-query-scan
```

출력은 아래와 같았다.

```text
point lookup plan: index-point-lookup (indexed equality predicate can jump directly to the leaf entry)
  row=4 handle=dina tier=gold
range scan plan: index-range-scan (indexed range predicate can walk linked leaves in key order)
  row=2 handle=ben region=emea
  row=3 handle=cora region=apac
  row=4 handle=dina region=na
  row=5 handle=erin region=na
fallback plan: full-scan (predicate is not aligned with the secondary index)
  row=1 handle=ada tier=gold
  row=4 handle=dina tier=gold
```

즉 이 프로젝트는 query planner를 "index를 쓸까 말까" 정도로만 남겨서, 전략 분기와 이유를 눈으로 바로 확인하게 만든다.

## 4. 추가 재실행으로 split 결과도 고정했다

이번에 project root 내부 임시 Go 파일로 추가 재실행을 돌린 결과는 아래였다.

```text
height_rootkeys 2 [cora erin] [4 99]
range_keys [ben cora dina erin]
plan_eq index-point-lookup
plan_range index-range-scan
plan_full full-scan
```

이 결과는 세 가지를 보여 준다.

- order `3`에서 insert를 계속하면 tree height가 `2`로 올라간다
- root separator key는 현재 `["cora", "erin"]`로 잡힌다
- duplicate key `dina`는 row id `[4, 99]`를 한 entry 아래 유지한다

즉 split이 일어나도 point lookup과 range ordering이 무너지지 않는다.
