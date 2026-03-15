# btree-index-and-query-scan 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

buffer pool 바로 위 단계에서 "정렬된 key를 어떻게 split하고 다시 찾을 것인가"를 구현한다. 여기서는 full SQL 엔진이 아니라, single-table row store에 secondary index 하나를 얹고 최소 planner까지 연결하는 데 집중한다. 핵심은 `main`와 `New`, `Insert` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- split 이후 point lookup과 duplicate key lookup이 모두 유지돼야 한다.
- range scan이 key order를 보존해야 한다.
- planner가 indexed column에는 index 전략을, 나머지 column에는 full scan 전략을 선택해야 한다.
- 첫 진입점은 `../go/database-internals/projects/08-btree-index-and-query-scan/cmd/btree-index-and-query-scan/main.go`이고, 여기서 `main`와 `New` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../go/database-internals/projects/08-btree-index-and-query-scan/cmd/btree-index-and-query-scan/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex/index.go`: `New`, `Insert`, `Lookup`, `OpenRange`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan/executor.go`: `New`, `Insert`, `Plan`, `Execute`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/08-btree-index-and-query-scan/tests/btree_index_test.go`: `TestSplitAndLookup`, `TestRangeCursorReturnsOrderedKeys`가 통과 조건과 회귀 포인트를 잠근다.
- `../go/database-internals/projects/08-btree-index-and-query-scan/tests/query_scan_test.go`: `TestPlannerUsesIndexForEqualityAndRange`, `TestPlannerFallsBackToFullScanForNonIndexedColumn`, `seededExecutor`가 통과 조건과 회귀 포인트를 잠근다.
- `main` 구현은 `TestSplitAndLookup` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan && GOWORK=off go test ./...`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../go/database-internals/projects/08-btree-index-and-query-scan/cmd/btree-index-and-query-scan/main.go`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `TestSplitAndLookup` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan && GOWORK=off go test ./...`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan && GOWORK=off go test ./...
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `TestSplitAndLookup`와 `TestRangeCursorReturnsOrderedKeys`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan && GOWORK=off go test ./...`로 회귀를 조기에 잡는다.

## 소스 근거

- `../go/database-internals/projects/08-btree-index-and-query-scan/cmd/btree-index-and-query-scan/main.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex/index.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan/executor.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/tests/btree_index_test.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/tests/query_scan_test.go`
