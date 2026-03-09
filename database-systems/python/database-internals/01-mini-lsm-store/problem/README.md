# Problem Framing

## Objective

Python 입문 트랙에서는 memtable 자료구조와 SSTable 형식을 별도 프로젝트로 나누지 않고, `put`, `get`, `delete`, `force flush`, `re-open`이 가능한 최소 LSM store 안에 함께 접는다.

## Requirements

- active MemTable이 threshold를 넘으면 immutable swap 후 SSTable로 flush한다.
- read path는 active memtable, immutable memtable, newest SSTable부터 차례로 조회한다.
- tombstone은 cross-level read에서도 delete 의미를 유지해야 한다.
- close 이후 re-open 시 기존 SSTable index를 다시 적재해야 한다.
- Python 프로젝트는 Go 트랙의 `01-memtable-skiplist`, `02-sstable-format`, `03-mini-lsm-store` 핵심 요구를 한 슬롯으로 압축한다.

## Source Provenance

- 원본 문제: `legacy/storage-engine/lsm-tree-core/problem/README.md`
- 원본 solution 참고: `legacy/storage-engine/lsm-tree-core/solve/solution/lsm-store.js`
- Python 재구성 이유: 입문 트랙의 진입 비용을 낮추기 위해 memtable과 SSTable prerequisite를 한 프로젝트로 접었다.
