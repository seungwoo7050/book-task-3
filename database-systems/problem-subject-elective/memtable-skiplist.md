# memtable-skiplist 문제지

## 왜 중요한가

Put(key, value)는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다. Get(key)는 존재하는 값, tombstone, 미존재를 구분해야 합니다. Delete(key)는 엔트리를 없애지 않고 tombstone으로 바꿔야 합니다. 전체 엔트리를 key 오름차순으로 순회할 수 있어야 합니다.

## 목표

시작 위치의 구현을 완성해 Put(key, value)는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다, Get(key)는 존재하는 값, tombstone, 미존재를 구분해야 합니다, Delete(key)는 엔트리를 없애지 않고 tombstone으로 바꿔야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go`
- `../go/database-internals/projects/01-memtable-skiplist/cmd/skiplist-demo/main.go`
- `../go/database-internals/projects/01-memtable-skiplist/internal/skiplist/skiplist.go`
- `../go/database-internals/projects/01-memtable-skiplist/tests/skiplist_test.go`

## starter code / 입력 계약

- ../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- Put(key, value)는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다.
- Get(key)는 존재하는 값, tombstone, 미존재를 구분해야 합니다.
- Delete(key)는 엔트리를 없애지 않고 tombstone으로 바꿔야 합니다.
- 전체 엔트리를 key 오름차순으로 순회할 수 있어야 합니다.

## 제외 범위

- `../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go` starter skeleton을 정답 구현으로 착각하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../go/database-internals/projects/01-memtable-skiplist/problem/code/skiplist.skeleton.go`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `main`와 `New`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestPutAndGet`와 `TestMissingKey`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/01-memtable-skiplist && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`memtable-skiplist_answer.md`](memtable-skiplist_answer.md)에서 확인한다.
