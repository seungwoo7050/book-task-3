# memtable-skiplist 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 Put(key, value)는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다, Get(key)는 존재하는 값, tombstone, 미존재를 구분해야 합니다, Delete(key)는 엔트리를 없애지 않고 tombstone으로 바꿔야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `New`, `newNode` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- Put(key, value)는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다.
- Get(key)는 존재하는 값, tombstone, 미존재를 구분해야 합니다.
- Delete(key)는 엔트리를 없애지 않고 tombstone으로 바꿔야 합니다.
- 첫 진입점은 `../go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go`이고, 여기서 `main`와 `New` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`: `New`, `newNode`, `randomLevel`, `Put`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go`: `New`, `Put`, `Delete`, `Get`가 핵심 흐름과 상태 전이를 묶는다.
- `../go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go`: `TestPutAndGet`, `TestMissingKey`, `TestUpdateKeepsLogicalSize`가 통과 조건과 회귀 포인트를 잠근다.
- `main` 구현은 `TestPutAndGet` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist && GOWORK=off go test ./...`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go`와 `../go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `TestPutAndGet` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist && GOWORK=off go test ./...`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist && GOWORK=off go test ./...
```

- `../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `TestPutAndGet`와 `TestMissingKey`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist && GOWORK=off go test ./...`로 회귀를 조기에 잡는다.

## 소스 근거

- `../go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go`
- `../go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`
- `../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go`
- `../go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go`
