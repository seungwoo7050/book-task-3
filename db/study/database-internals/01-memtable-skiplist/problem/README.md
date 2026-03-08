# Problem Framing

## Objective

정렬된 문자열 키-값 엔트리를 저장하는 MemTable용 SkipList를 구현한다. 이 프로젝트는 레거시 `lsm-tree-core`에서 SkipList 부분만 분리한 학습 단위다.

## Requirements

### R1 Sorted Insert

- 키는 사전식 순서로 유지된다.
- `Put(key, value)`는 새 키를 삽입하거나 기존 키를 갱신한다.

### R2 Lookup

- `Get(key)`는 세 상태를 구분해야 한다.
- 존재하는 값
- tombstone
- 미존재

### R3 Tombstone

- `Delete(key)`는 엔트리를 물리 삭제하지 않고 tombstone으로 바꾼다.
- tombstone은 iteration과 size accounting에 남아 있어야 한다.

### R4 Ordered Iteration

- 전체 엔트리를 key 오름차순으로 순회할 수 있어야 한다.
- 이후 SSTable flush가 이 순서에 의존한다.

### R5 Byte Size Tracking

- MemTable이 flush threshold를 넘는지 판단할 수 있도록 대략적 byte size를 추적한다.

## Constraints

- 키와 값은 UTF-8 문자열이다.
- 동시성 제어는 요구하지 않는다.
- 외부 라이브러리는 사용하지 않는다.

## Source Provenance

- 원본 문제: `legacy/storage-engine/lsm-tree-core/problem/README.md`
- 원본 starter code: `legacy/storage-engine/lsm-tree-core/problem/code/skiplist.skeleton.js`
- 이 프로젝트는 레거시 문제의 `R1 — MemTable`에 해당하는 부분만 분리했다.
- 새 `problem/code/skiplist.skeleton.go`는 원본 JS skeleton의 학습 범위를 Go API로 옮긴 보조 스타터다. 원본 파일 자체의 복제본은 아니다.

