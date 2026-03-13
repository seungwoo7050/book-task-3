# Database Internals

아래 표는 각 독립 프로젝트를 기존 초안과 분리한 뒤 source-first로 다시 쓴 시리즈 입구다.

| 프로젝트 | 시리즈 맵 | 재검증 신호 |
| --- | --- | --- |
| 01 MemTable SkipList | [00-series-map.md](01-memtable-skiplist/00-series-map.md) | `go test ok, 9 tests`, demo `size=3 byteSize=220` |
| 02 SSTable Format | [00-series-map.md](02-sstable-format/00-series-map.md) | `go test ok, 6 tests`, demo `missing => <missing>` |
| 03 Mini LSM Store | [00-series-map.md](03-mini-lsm-store/00-series-map.md) | `go test ok, 9 tests`, demo `missing => <missing>` |
| 04 WAL Recovery | [00-series-map.md](04-wal-recovery/00-series-map.md) | `go test ok, 7 tests`, demo `missing => <missing>` |
| 05 Leveled Compaction | [00-series-map.md](05-leveled-compaction/00-series-map.md) | `go test ok, 4 tests`, demo `pear=green` |
| 06 Index Filter | [00-series-map.md](06-index-filter/00-series-map.md) | `go test ok, 4 tests`, demo `durian=gold bytes_read=74` |
| 07 Buffer Pool | [00-series-map.md](07-buffer-pool/00-series-map.md) | `go test ok, 7 tests`, demo `page-1` |
| 08 MVCC | [00-series-map.md](08-mvcc/00-series-map.md) | `go test ok, 7 tests`, demo `t2 sees x=v1` |
