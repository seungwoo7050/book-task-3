# Database Internals Track

Python 저장 엔진 트랙은 더 적은 프로젝트 수로 LSM, durability, read-path optimization, cache, MVCC를 먼저 익히는 입문 경로입니다.

## 읽기 전에 알면 좋은 것

- 저장 엔진 전체 흐름을 빠르게 잡고 싶은 학습자에게 적합합니다.
- 세부 구현을 더 깊게 보고 싶어지면 Go 대응 프로젝트로 내려가면 됩니다.

## 추천 순서

| 순서 | 프로젝트 | 이 단계에서 보는 질문 | 다음 단계 |
| --- | --- | --- | --- |
| 1 | [`01-mini-lsm-store`](01-mini-lsm-store/README.md) | write path와 read path를 하나의 작은 LSM store로 연결하는 단계 | 02 WAL Recovery |
| 2 | [`02-wal-recovery`](02-wal-recovery/README.md) | durable write path와 crash recovery를 붙이는 단계 | 03 Index Filter |
| 3 | [`03-index-filter`](03-index-filter/README.md) | 없는 key를 빨리 거절하고 있는 key 범위만 읽는 최적화 단계 | 04 Buffer Pool |
| 4 | [`04-buffer-pool`](04-buffer-pool/README.md) | page cache, eviction, write-back 정책을 배우는 단계 | 05 MVCC |
| 5 | [`05-mvcc`](05-mvcc/README.md) | version visibility와 write-write conflict를 배우는 트랜잭션 단계 | Python DDIA track or your own transaction extension |

## 이 트랙을 끝내면 남는 것

- 각 프로젝트가 어떤 설계 질문을 던지는지 한 번의 경로로 따라갈 수 있습니다.
- 각 README 마지막 섹션을 통해 공개용 포트폴리오로 확장할 수 있는 방향을 바로 확인할 수 있습니다.

## 다음 단계

이 트랙을 끝낸 뒤 Go 저장 엔진 트랙으로 내려가면 세분화된 구현 차이가 선명하게 보입니다.
