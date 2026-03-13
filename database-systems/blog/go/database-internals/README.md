# Database Internals

메모리 자료구조에서 시작해 flush, recovery, compaction, buffer, MVCC까지 저장 엔진 내부 규칙을 한 단계씩 넓혀 갑니다.

## 처음 읽는다면

- 가장 작은 진입점: [01 MemTable SkipList](01-memtable-skiplist/00-series-map.md)
- 저장 엔진 표면을 빨리 보고 싶다면: [03 Mini LSM Store](03-mini-lsm-store/00-series-map.md)
- 뒤쪽 경계까지 가고 싶다면: [08 BTree Index And Query Scan](08-btree-index-and-query-scan/00-series-map.md) -> [09 MVCC](09-mvcc/00-series-map.md)

## 프로젝트 지도

| 프로젝트 | 한 줄 설명 | 재검증 신호 | 시리즈 |
| --- | --- | --- | --- |
| 01 MemTable SkipList | LSM-Tree의 active memtable을 독립적인 SkipList로 구현해 정렬된 쓰기 경로와 tombstone semantics를 먼저 고정합니다. | `go test ok, 9 tests`, demo `size=3 byteSize=220` | [00-series-map.md](01-memtable-skiplist/00-series-map.md) |
| 02 SSTable Format | immutable SSTable 파일 형식, sparse key index, footer metadata를 구현해 on-disk lookup의 기본을 고정합니다. | `go test ok, 6 tests`, demo `missing => <missing>` | [00-series-map.md](02-sstable-format/00-series-map.md) |
| 03 Mini LSM Store | active memtable, immutable flush, newest-first read path를 연결해 최소 LSM store를 완성합니다. | `go test ok, 9 tests`, demo `missing => <missing>` | [00-series-map.md](03-mini-lsm-store/00-series-map.md) |
| 04 WAL Recovery | append-before-apply WAL과 replay 기반 recovery를 구현해 durable write path를 만듭니다. | `go test ok, 7 tests`, demo `missing => <missing>` | [00-series-map.md](04-wal-recovery/00-series-map.md) |
| 05 Leveled Compaction | L0의 겹치는 SSTable을 병합하고 manifest를 원자적으로 갱신해 leveled compaction의 핵심만 구현합니다. | `go test ok, 4 tests`, demo `pear=green` | [00-series-map.md](05-leveled-compaction/00-series-map.md) |
| 06 Index Filter | Bloom filter와 sparse index를 붙여 point lookup이 전체 SSTable 스캔으로 떨어지지 않도록 만듭니다. | `go test ok, 4 tests`, demo `durian=gold bytes_read=74` | [00-series-map.md](06-index-filter/00-series-map.md) |
| 07 Buffer Pool | disk-backed page를 메모리에 캐시하고 pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현합니다. | `go test ok, 7 tests`, demo `page-1` | [00-series-map.md](07-buffer-pool/00-series-map.md) |
| 08 BTree Index And Query Scan | B+Tree leaf split, linked range cursor, rule-based query scan으로 buffer pool 위의 read path를 확장합니다. | `go test ok, 6 tests`, demo `full-scan rows=2 index rows=2 range rows=3` | [00-series-map.md](08-btree-index-and-query-scan/00-series-map.md) |
| 09 MVCC | snapshot isolation을 위한 version chain과 transaction manager를 구현합니다. | `go test ok, 7 tests`, demo `t2 sees x=v1` | [00-series-map.md](09-mvcc/00-series-map.md) |
