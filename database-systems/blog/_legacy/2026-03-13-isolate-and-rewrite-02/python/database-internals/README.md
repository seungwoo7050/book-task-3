# Database Internals

아래 표는 각 독립 프로젝트를 기존 초안과 분리한 뒤 source-first로 다시 쓴 시리즈 입구다.

| 프로젝트 | 시리즈 맵 | 재검증 신호 |
| --- | --- | --- |
| 01 Mini LSM Store | [00-series-map.md](01-mini-lsm-store/00-series-map.md) | `9 passed`, demo `{'key': 'alpha', 'found': True, 'value': '3', 'sstables': 1}` |
| 02 WAL Recovery | [00-series-map.md](02-wal-recovery/00-series-map.md) | `7 passed`, demo `{'recovered': True, 'value': '1'}` |
| 03 Index Filter | [00-series-map.md](03-index-filter/00-series-map.md) | `4 passed`, demo `{'found': True, 'value': 'value-k023', 'bytes_read': 176}` |
| 04 Buffer Pool | [00-series-map.md](04-buffer-pool/00-series-map.md) | `7 passed`, demo `{'page_id': '/var/folders/92/jftxv3md5_z3jr5ybm1c3yx40000gn/T/buffer-pool-gg0isyxk/data.db` |
| 05 MVCC | [00-series-map.md](05-mvcc/00-series-map.md) | `7 passed`, demo `{'tx': 1, 'read_your_own_write': 10}` |
