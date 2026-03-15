# Core Invariants

## 1. duplicate key는 separate entry가 아니라 row-id list에 append된다

`insertIntoLeaf()`는 같은 key를 다시 만나면 새 entry를 만들지 않는다. 기존 entry의 `RowIDs`에 append만 한다.

```go
if entryIndex < len(leaf.entries) && leaf.entries[entryIndex].Key == key {
    leaf.entries[entryIndex].RowIDs = append(leaf.entries[entryIndex].RowIDs, rowID)
    return nil
}
```

즉 secondary index에서 duplicate key는 정상 상태다. point lookup이 단일 row가 아니라 row-id list를 돌려줄 수 있어야 planner가 indexed equality에도 여러 row를 반환할 수 있다.

## 2. leaf split은 오른쪽 leaf 첫 key를 부모에 올린다

leaf overflow가 나면 `insertIntoLeaf()`는 절반을 오른쪽 leaf로 옮기고, `right.entries[0].Key`를 promoted key로 돌려준다.

```go
return &splitResult{
    promotedKey: right.entries[0].Key,
    right:       right,
}
```

docs의 [`b-plus-tree-page-splits.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/docs/concepts/b-plus-tree-page-splits.md)가 설명하는 separator rule이 그대로 구현된 것이다.

추가 재실행에서 `height_rootkeys 2 [cora erin] ...`가 나온 것도 이 split 규칙의 결과다.

## 3. range cursor는 linked leaf를 따라가며 end boundary를 넘는 순간 멈춘다

`OpenRange(start, end)`는 `seek(start)`로 첫 leaf와 entry index를 찾고, `RangeCursor.Next()`는 다음 leaf로 넘어가며 순회한다.

핵심 종료 조건은 아래다.

```go
if cursor.end != "" && entry.Key > cursor.end {
    return Entry{}, false
}
```

즉 range scan은 sorted leaf chain 위에서 key order를 보존한 채 `start <= key <= end` 범위를 정확히 잘라낸다. 추가 재실행의 `range_keys [ben cora dina erin]`가 그 계약을 직접 보여 준다.

## 4. planner는 cost를 계산하지 않고 predicate shape만 본다

`Plan()`은 딱 세 분기만 가진다.

- indexed equality -> `index-point-lookup`
- indexed range -> `index-range-scan`
- 그 외 -> `full-scan`

즉 이 planner는 cardinality나 cost를 모른다. 하지만 그 대신 "왜 이 predicate가 index를 탈 수 있는가"를 한 줄 `Reason`으로 설명한다. docs의 [`range-cursor-and-rule-based-planner.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan/docs/concepts/range-cursor-and-rule-based-planner.md)가 바로 이 작은 다리를 설명한다.

## 5. source-only nuance: insert는 empty key를 조용히 버린다

`BTreeIndex.Insert()`의 첫 줄은 아래 조건이다.

```go
if key == "" {
    return
}
```

즉 빈 indexed key는 별도 에러 없이 그냥 무시된다. 테스트는 이 경계를 직접 다루지 않지만, 현재 구현이 strict validation보다 minimal lab semantics를 택했다는 점을 보여 주는 작은 신호다.
