# Database Internals Track

Go 저장 엔진 정본 트랙입니다. 자료구조, 파일 포맷, durability, compaction, cache, MVCC를 가장 세밀하게 분해합니다.

## 누가 여기서 시작해야 하는가

- Python 저장 엔진 트랙을 끝낸 뒤 자료구조와 파일 포맷을 더 세밀하게 다시 읽고 싶은 사람에게 맞습니다.
- write structure, immutable format, recovery, compaction을 각각 독립된 학습 슬롯으로 분리해 따라가고 싶은 사람에게 맞습니다.
- 각 행의 `문제`, `내 해법`, `검증`은 [전역 카탈로그](../../docs/catalog/project-catalog.md)와 같은 문구를 사용합니다.

## 이 트랙이 답하는 질문

- 정렬된 write structure와 immutable file format을 어떻게 이어 붙일 것인가
- flush, recovery, compaction, buffer pool, MVCC가 저장 엔진 안에서 어떤 순서로 이어지는가

## 프로젝트 표

| 프로젝트 | 문제 | 내 해법 | 검증 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [01 MemTable SkipList](projects/01-memtable-skiplist/README.md) | `Put(key, value)`는 새 키를 삽입하거나 기존 키를 갱신하면서 key 오름차순을 유지해야 합니다. | 정렬된 문자열 키-값 엔트리를 유지하는 in-memory write structure를 설계합니다. | `go test ./...`<br>`go run ./cmd/skiplist-demo` | SSTable Format |
| [02 SSTable Format](projects/02-sstable-format/README.md) | data section은 key 오름차순 record의 연속 바이트 배열이어야 합니다. | 정렬된 record stream을 immutable file format으로 저장하는 방법을 익힙니다. | `go test ./...`<br>`go run ./cmd/sstable-format` | Mini LSM Store |
| [03 Mini LSM Store](projects/03-mini-lsm-store/README.md) | active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다. | active memtable이 threshold를 넘을 때 immutable swap과 flush가 어떻게 이어지는지 익힙니다. | `go test ./...`<br>`go run ./cmd/mini-lsm-store` | WAL Recovery |
| [04 WAL Recovery](projects/04-wal-recovery/README.md) | PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다. | acknowledged write를 잃지 않기 위한 append-before-apply 순서를 익힙니다. | `go test ./...`<br>`go run ./cmd/wal-recovery` | Leveled Compaction |
| [05 Leveled Compaction](projects/05-leveled-compaction/README.md) | 입력 source 배열에서 newer-first 우선순위를 유지한 k-way merge를 수행해야 합니다. | newest-first 우선순위를 유지한 k-way merge를 구현합니다. | `go test ./...`<br>`go run ./cmd/leveled-compaction` | Index Filter |
| [06 Index Filter](projects/06-index-filter/README.md) | Bloom filter를 직렬화·복원할 수 있어야 합니다. | Bloom filter가 negative lookup 비용을 어떻게 줄이는지 이해합니다. | `go test ./...`<br>`go run ./cmd/index-filter` | Buffer Pool |
| [07 Buffer Pool](projects/07-buffer-pool/README.md) | page id로 file path와 page number를 안정적으로 분리해야 합니다. | 고정 크기 page를 메모리에 캐시하는 기본 구조를 익힙니다. | `go test ./...`<br>`go run ./cmd/buffer-pool` | MVCC |
| [08 MVCC](projects/08-mvcc/README.md) | snapshot isolation 하에서 읽기 스냅샷과 write-write conflict를 관리해야 합니다. | snapshot timestamp가 어떤 version을 볼 수 있는지 판단하는 규칙을 익힙니다. | `go test ./...`<br>`go run ./cmd/mvcc` | 자체 확장 프로젝트 |

## 다음 단계

- 각 프로젝트는 `README -> problem/README -> docs/README -> 구현 -> tests -> notion/README` 순서로 읽습니다.
- 이 트랙 뒤에는 [Go 분산 트랙](../ddia-distributed-systems/README.md)의 capstone, quorum, election 슬롯으로 넘어가면 저장 엔진 관점이 더 선명해집니다.
