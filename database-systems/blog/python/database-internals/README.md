# Database Internals

메모리 자료구조에서 시작해 flush, recovery, compaction, buffer, MVCC까지 저장 엔진 내부 규칙을 한 단계씩 넓혀 갑니다.

## 처음 읽는다면

- 가장 작은 진입점: [01 Mini LSM Store](01-mini-lsm-store/00-series-map.md)
- 저장 엔진 표면을 빨리 보고 싶다면: [03 Index Filter](03-index-filter/00-series-map.md)
- 뒤쪽 경계까지 가고 싶다면: [05 MVCC](05-mvcc/00-series-map.md)

## 프로젝트 지도

| 프로젝트 | 한 줄 설명 | 재검증 신호 | 시리즈 |
| --- | --- | --- | --- |
| 01 Mini LSM Store | active memtable, immutable flush, newest-first read path를 연결해 최소 LSM store를 완성합니다. | `9 passed`, demo `{'key': 'alpha', 'found': True, 'value': '3', 'sstables': 1}` | [00-series-map.md](01-mini-lsm-store/00-series-map.md) |
| 02 WAL Recovery | append-before-apply WAL과 replay 기반 recovery를 구현해 durable write path를 만듭니다. | `7 passed`, demo `{'recovered': True, 'value': '1'}` | [00-series-map.md](02-wal-recovery/00-series-map.md) |
| 03 Index Filter | Bloom filter와 sparse index를 붙여 point lookup이 전체 SSTable 스캔으로 떨어지지 않도록 만듭니다. | `4 passed`, demo `{'found': True, 'value': 'value-k023', 'bytes_read': 176}` | [00-series-map.md](03-index-filter/00-series-map.md) |
| 04 Buffer Pool | disk-backed page를 메모리에 캐시하고 pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현합니다. | `7 passed`, demo `{'page_id': '/var/folders/92/jftxv3md5_z3jr5ybm1c3yx40000gn/T/buffer-pool-l8i1fl_2/data.db` | [00-series-map.md](04-buffer-pool/00-series-map.md) |
| 05 MVCC | snapshot isolation을 위한 version chain과 transaction manager를 구현합니다. | `7 passed`, demo `{'tx': 1, 'read_your_own_write': 10}` | [00-series-map.md](05-mvcc/00-series-map.md) |
