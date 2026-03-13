# Database Internals Blog Series

저장 엔진 입문 트랙을 "기능 목록"이 아니라 "판단 전환의 연속"으로 읽기 위한 인덱스다.

| 프로젝트 | 시리즈 입구 | 재검증 신호 |
| --- | --- | --- |
| 01 Mini LSM Store | [00-series-map.md](01-mini-lsm-store/00-series-map.md) | `9 passed`, demo `alpha -> 3` |
| 02 WAL Recovery | [00-series-map.md](02-wal-recovery/00-series-map.md) | `7 passed`, demo `recovered=True` |
| 03 Index Filter | [00-series-map.md](03-index-filter/00-series-map.md) | `4 passed`, demo `bytes_read=176` |
| 04 Buffer Pool | [00-series-map.md](04-buffer-pool/00-series-map.md) | `7 passed`, demo `pin_count=1` |
| 05 MVCC | [00-series-map.md](05-mvcc/00-series-map.md) | `7 passed`, demo `read_your_own_write=10` |

## 읽기 권장 순서

`01 -> 02 -> 03 -> 04 -> 05`

write path와 durability를 먼저 고정한 뒤, lookup 최적화, page cache, version visibility로 올라가는 흐름이 가장 자연스럽다.
