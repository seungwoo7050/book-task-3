# Database Internals Track

Go 저장 엔진 트랙은 자료구조, 파일 포맷, flush orchestration, durability, transaction까지를 가장 세밀하게 나눠 따라가는 전체 경로입니다.

## 읽기 전에 알면 좋은 것

- 정렬 자료구조와 파일 I/O 기초를 알고 있으면 좋습니다.
- 각 단계가 작게 나뉘므로 프로젝트 간 연결을 스스로 메모해 가며 읽으면 좋습니다.

## 추천 순서

| 순서 | 프로젝트 | 이 단계에서 보는 질문 | 다음 단계 |
| --- | --- | --- | --- |
| 1 | [`01-memtable-skiplist`](01-memtable-skiplist/README.md) | 정렬된 memtable과 tombstone semantics를 먼저 고정하는 출발점 | 02 SSTable Format |
| 2 | [`02-sstable-format`](02-sstable-format/README.md) | immutable file format과 lookup metadata를 분리해서 학습하는 단계 | 03 Mini LSM Store |
| 3 | [`03-mini-lsm-store`](03-mini-lsm-store/README.md) | write path와 read path를 하나의 작은 LSM store로 연결하는 단계 | 04 WAL Recovery |
| 4 | [`04-wal-recovery`](04-wal-recovery/README.md) | durable write path와 crash recovery를 붙이는 단계 | 05 Leveled Compaction |
| 5 | [`05-leveled-compaction`](05-leveled-compaction/README.md) | compaction merge와 manifest atomicity를 배우는 심화 단계 | 06 Index Filter |
| 6 | [`06-index-filter`](06-index-filter/README.md) | 없는 key를 빨리 거절하고 있는 key 범위만 읽는 최적화 단계 | 07 Buffer Pool |
| 7 | [`07-buffer-pool`](07-buffer-pool/README.md) | page cache, eviction, write-back 정책을 배우는 단계 | 08 MVCC |
| 8 | [`08-mvcc`](08-mvcc/README.md) | version visibility와 write-write conflict를 배우는 트랜잭션 단계 | Go DDIA track or your own storage-engine extension |

## 이 트랙을 끝내면 남는 것

- 각 프로젝트가 어떤 설계 질문을 던지는지 한 번의 경로로 따라갈 수 있습니다.
- 각 README 마지막 섹션을 통해 공개용 포트폴리오로 확장할 수 있는 방향을 바로 확인할 수 있습니다.

## 다음 단계

저장 엔진 트랙을 끝내면 Go 분산 트랙 capstone에서 local storage 관점을 더 잘 읽을 수 있습니다.
