# Problem - BTree Index And Query Scan

buffer pool 바로 위 단계에서 "정렬된 key를 어떻게 split하고 다시 찾을 것인가"를 구현한다. 여기서는 full SQL 엔진이 아니라, single-table row store에 secondary index 하나를 얹고 최소 planner까지 연결하는 데 집중한다.

## 요구 사항

- B+Tree leaf insert가 key 오름차순을 유지해야 한다.
- leaf가 꽉 차면 sibling leaf를 만들고 부모에 separator key를 올려야 한다.
- duplicate key는 같은 leaf entry 아래 row id list로 유지해야 한다.
- range cursor는 linked leaf를 따라 `start <= key <= end` 범위를 key order로 순회해야 한다.
- query planner는 indexed equality, indexed range, non-indexed predicate를 구분해야 한다.

## 성공 기준

- split 이후 point lookup과 duplicate key lookup이 모두 유지돼야 한다.
- range scan이 key order를 보존해야 한다.
- planner가 indexed column에는 index 전략을, 나머지 column에는 full scan 전략을 선택해야 한다.
- demo CLI에서 point lookup, range scan, fallback full scan 세 경우를 모두 보여 줘야 한다.

## 일부러 하지 않는 것

- delete merge / redistribution
- cost-based optimizer
- join, aggregate, projection pushdown
- transaction visibility와 lock manager
