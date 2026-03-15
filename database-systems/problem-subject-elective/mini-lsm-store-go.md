# mini-lsm-store-go 문제지

## 왜 중요한가

active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다. read path는 active memtable, immutable memtable, newest SSTable부터 순서대로 조회해야 합니다. tombstone은 cross-level read에서도 삭제 의미를 유지해야 합니다. close 이후 re-open 시 기존 SSTable index를 다시 적재해야 합니다.

## 목표

시작 위치의 구현을 완성해 active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다, read path는 active memtable, immutable memtable, newest SSTable부터 순서대로 조회해야 합니다, tombstone은 cross-level read에서도 삭제 의미를 유지해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../go/database-internals/projects/03-mini-lsm-store/cmd/mini-lsm-store/main.go`
- `../go/database-internals/projects/03-mini-lsm-store/internal/lsmstore/store.go`
- `../go/database-internals/projects/03-mini-lsm-store/internal/skiplist/skiplist.go`
- `../go/database-internals/projects/03-mini-lsm-store/internal/sstable/sstable.go`
- `../go/database-internals/projects/03-mini-lsm-store/tests/lsm_store_test.go`

## starter code / 입력 계약

- `../go/database-internals/projects/03-mini-lsm-store/cmd/mini-lsm-store/main.go`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다.
- read path는 active memtable, immutable memtable, newest SSTable부터 순서대로 조회해야 합니다.
- tombstone은 cross-level read에서도 삭제 의미를 유지해야 합니다.
- close 이후 re-open 시 기존 SSTable index를 다시 적재해야 합니다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `printLookup`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestPutAndGet`와 `TestMissingKey`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store && GOWORK=off go test ./...`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/03-mini-lsm-store && GOWORK=off go test ./...
```

- Go 계열 검증은 `go` toolchain과 필요한 module checksum(`go.sum`)이 준비돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`mini-lsm-store-go_answer.md`](mini-lsm-store-go_answer.md)에서 확인한다.
