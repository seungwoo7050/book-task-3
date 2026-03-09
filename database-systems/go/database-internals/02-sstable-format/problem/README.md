# Problem Framing

## Objective

sorted key-value record를 immutable binary file로 저장하고, footer에 담긴 index section을 사용해 특정 key를 빠르게 찾는다.

## Requirements

- data section은 key 오름차순 record들의 연속 바이트 배열이어야 한다.
- index section은 `(key, offset)` 쌍을 저장해 point lookup의 시작 위치를 알려야 한다.
- footer는 `dataSectionSize`와 `indexSectionSize`를 8바이트에 기록해야 한다.
- tombstone은 value length sentinel로 보존되어야 한다.
- file reopen 이후에도 `LoadIndex`와 `Lookup`이 동작해야 한다.

## Source Provenance

- 원본 문제: `legacy/storage-engine/lsm-tree-core/problem/README.md`
- 원본 starter code: `legacy/storage-engine/lsm-tree-core/problem/code/sstable.skeleton.js`
- 원본 solution 참고: `legacy/storage-engine/lsm-tree-core/solve/solution/sstable.js`
- 분할 이유: MemTable 자료구조와 flush orchestration을 떼어내고 file format 자체를 별도로 검증하기 위해서다.

