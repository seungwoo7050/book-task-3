# Problem Framing

## Objective

MemTable과 SSTable을 묶어 `put`, `get`, `delete`, `force flush`, `re-open`이 가능한 최소 LSM store를 구현한다.

## Requirements

- active MemTable이 threshold를 넘으면 immutable swap 후 SSTable로 flush한다.
- read path는 active memtable, immutable memtable, newest SSTable부터 차례로 조회한다.
- tombstone은 cross-level read에서도 delete 의미를 유지해야 한다.
- close 이후 re-open 시 기존 SSTable index를 다시 적재해야 한다.

## Source Provenance

- 원본 문제: `legacy/storage-engine/lsm-tree-core/problem/README.md`
- 원본 solution 참고: `legacy/storage-engine/lsm-tree-core/solve/solution/lsm-store.js`
- 분할 이유: SkipList와 SSTable을 익힌 뒤 orchestration만 독립적으로 검증하기 위해서다.

