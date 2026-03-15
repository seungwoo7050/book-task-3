# Verification And Boundaries

## 1. 자동 검증은 split, duplicate key, planner 분기를 함께 덮는다

2026-03-14 기준 재실행 명령은 아래와 같다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan
GOWORK=off go test ./...
```

결과는 아래처럼 통과했다.

```text
ok  	study.local/go/database-internals/projects/08-btree-index-and-query-scan/tests	(cached)
```

테스트가 잡는 항목은 아래와 같다.

- split 뒤 tree height 증가
- duplicate key lookup
- missing lookup
- ordered range cursor
- equality/range planner의 index 선택
- non-indexed predicate의 full-scan fallback

즉 index semantics와 planner semantics를 함께 확인한다.

다만 planner coverage를 더 정확히 말하면 single-column exact/range/non-indexed fallback까지만 잠근다. "이 range가 너무 넓으니 full scan이 더 낫다" 같은 선택은 현재 테스트도, 구현도 다루지 않는다.

## 2. demo와 추가 재실행 관찰값

demo 출력의 핵심:

- point lookup은 `index-point-lookup`
- range scan은 `index-range-scan`
- `tier=gold`는 `full-scan`

추가 재실행 출력:

```text
height_rootkeys 2 [cora erin] [4 99]
range_keys [ben cora dina erin]
plan_eq index-point-lookup
plan_range index-range-scan
plan_full full-scan
```

이 결과를 합치면 현재 구현은 아래 사실을 만족한다.

- split 이후에도 duplicate key row-id list는 유지된다
- linked leaf range scan은 key order를 보존한다
- planner는 indexed column 여부와 predicate shape만으로 전략을 나눈다
- 그 말은 반대로 row 수, selectivity, range 폭은 지금 전혀 비용 비교에 들어오지 않는다는 뜻이기도 하다

## 3. 현재 구현이 일부러 다루지 않는 것

이 랩을 query engine 완성본으로 읽으면 안 된다.

- delete merge / redistribution이 없다
- cost-based optimizer가 없다
- wide range vs narrow range를 구분하는 heuristic도 없다
- join, aggregate, projection pushdown이 없다
- transaction visibility와 lock manager가 없다
- buffer pool pin/unpin과 실제 page layout이 직접 연결돼 있지 않다

또 하나 분명히 남길 점은 Query model 자체가 작다는 것이다. 현재 `Query`는 `Column + Exact/Start/End` 하나만 가진다. 다중 predicate, conjunction/disjunction, covering index 같은 planner 고민은 아예 표현 단계에 들어오지 않는다.

즉 이 프로젝트는 index structure와 작은 planner 사이의 최소 연결점만 보여 준다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 쓰지 않았다.

- "B+Tree DB 엔진을 완성했다"
- "query optimizer를 구현했다"
- "disk page 기반 index manager까지 다 연결했다"

현재 소스와 테스트가 실제로 보여 주는 것은 in-memory B+Tree split, duplicate key row-id list, linked-leaf range scan, rule-based full-scan fallback까지다. 그보다 큰 엔진 claim은 근거가 없다.
