# Database Internals Track

Python 저장 엔진 입문 트랙입니다. 더 적은 프로젝트 수로 write path, durability, read-path optimization, cache, MVCC의 큰 흐름을 먼저 잡습니다.

## 누가 여기서 시작해야 하는가

- 저장 엔진을 처음 공부하며 write path, durability, cache, MVCC의 큰 흐름을 먼저 고정하고 싶은 사람에게 맞습니다.
- Go 정본 트랙으로 내려가기 전에 self-contained한 프로젝트 몇 개로 전체 구조를 잡고 싶은 사람에게 맞습니다.
- 각 행의 `문제`, `내 해법`, `검증`은 [전역 카탈로그](../../docs/catalog/project-catalog.md)와 같은 문구를 사용합니다.

## 이 트랙이 답하는 질문

- 저장 엔진의 write path와 read path를 가장 적은 프로젝트 수로 어떻게 이해할 것인가
- Go 심화 트랙으로 내려가기 전에 어떤 핵심 개념을 먼저 고정해야 하는가
- source-first 관점에서 각 프로젝트의 설계 판단과 검증 흐름을 어떻게 다시 읽을 것인가

## 프로젝트 표

| 프로젝트 | 문제 | 내 해법 | 검증 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [01 Mini LSM Store](projects/01-mini-lsm-store/README.md) | active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다. | active memtable이 threshold를 넘을 때 immutable swap과 flush가 어떻게 이어지는지 익힙니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m mini_lsm_store` | WAL Recovery |
| [02 WAL Recovery](projects/02-wal-recovery/README.md) | PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다. | acknowledged write를 잃지 않기 위한 append-before-apply 순서를 익힙니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m wal_recovery` | Index Filter |
| [03 Index Filter](projects/03-index-filter/README.md) | Bloom filter를 직렬화·복원할 수 있어야 합니다. | Bloom filter가 negative lookup 비용을 어떻게 줄이는지 이해합니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m index_filter` | Buffer Pool |
| [04 Buffer Pool](projects/04-buffer-pool/README.md) | page id로 file path와 page number를 안정적으로 분리해야 합니다. | 고정 크기 page를 메모리에 캐시하는 기본 구조를 익힙니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m buffer_pool` | MVCC |
| [05 MVCC](projects/05-mvcc/README.md) | snapshot isolation 하에서 읽기 스냅샷과 write-write conflict를 관리해야 합니다. | snapshot timestamp가 어떤 version을 볼 수 있는지 판단하는 규칙을 익힙니다. | `PYTHONPATH=src python -m pytest`<br>`PYTHONPATH=src python -m mvcc_lab` | Go 심화 슬롯 |

## 다음 단계

- 각 프로젝트는 `README -> problem/README -> docs/README -> 구현 -> tests -> notion/README` 순서로 읽습니다.
- source-first chronology로 다시 읽고 싶다면 [../../blog/python/database-internals/README.md](../../blog/python/database-internals/README.md)에서 각 프로젝트의 `00-series-map.md`로 이동합니다.
- 이 트랙을 끝낸 뒤 [Go 저장 엔진 트랙](../../go/database-internals/README.md)으로 내려가면 자료구조와 파일 포맷을 더 세밀하게 비교할 수 있습니다.
