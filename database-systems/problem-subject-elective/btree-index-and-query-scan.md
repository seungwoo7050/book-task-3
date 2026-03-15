# btree-index-and-query-scan 문제지

## 왜 중요한가

buffer-pool이 page를 붙잡는 쪽이었다면, 이번 단계는 그 page 위에서 key order를 어떻게 유지할지 보는 쪽이다. 범위는 B+Tree insert/split, duplicate key lookup, linked-leaf range scan, 그리고 "언제 index를 타고 언제 full scan으로 내려갈지"를 고르는 rule-based planner까지로 제한했다.

## 목표

buffer pool 바로 위 단계에서 "정렬된 key를 어떻게 split하고 다시 찾을 것인가"를 구현한다. 여기서는 full SQL 엔진이 아니라, single-table row store에 secondary index 하나를 얹고 최소 planner까지 연결하는 데 집중한다.

## 시작 위치

- `../go/database-internals/projects/08-btree-index-and-query-scan/cmd/btree-index-and-query-scan/main.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/internal/btreeindex/index.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/internal/queryscan/executor.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/tests/btree_index_test.go`
- `../go/database-internals/projects/08-btree-index-and-query-scan/tests/query_scan_test.go`

## starter code / 입력 계약

- `../go/database-internals/projects/08-btree-index-and-query-scan/cmd/btree-index-and-query-scan/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- split 이후 point lookup과 duplicate key lookup이 모두 유지돼야 한다.
- range scan이 key order를 보존해야 한다.
- planner가 indexed column에는 index 전략을, 나머지 column에는 full scan 전략을 선택해야 한다.
- demo CLI에서 point lookup, range scan, fallback full scan 세 경우를 모두 보여 줘야 한다.

## 제외 범위

- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `New`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestSplitAndLookup`와 `TestRangeCursorReturnsOrderedKeys`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/08-btree-index-and-query-scan && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`btree-index-and-query-scan_answer.md`](btree-index-and-query-scan_answer.md)에서 확인한다.
