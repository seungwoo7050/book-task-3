# 문제 프레이밍

## 왜 이 프로젝트를 하는가
flush 이전의 memtable 상태를 WAL에 먼저 기록하고, crash 이후 replay로 복원하는 durability 기본기를 익히는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Go
- 이전 단계: 03 Mini LSM Store
- 다음 단계: 05 Leveled Compaction
- 지금 답하려는 질문: 메모리 상태가 사라진 뒤에도 마지막 정상 record까지 재구성하려면 WAL은 어떤 순서와 어떤 검증 규칙을 가져야 하는가?

## 이번 구현에서 성공으로 보는 것
- put/delete 연산이 WAL에 append된 뒤 메모리 상태에 반영되어야 합니다.
- 재시작 시 WAL replay만으로 마지막 정상 상태를 복원할 수 있어야 합니다.
- 손상되었거나 잘린 trailing record가 있으면 그 지점에서 안전하게 멈춰야 합니다.
- delete는 live value 제거가 아니라 tombstone replay로 해석되어야 합니다.
- flush 이후에는 새 SSTable이 만들어지고 active WAL이 회전되어야 합니다.

## 먼저 열어 둘 파일
- `../internal/store/store.go`: `DurableStore`가 WAL, memtable, flush를 함께 묶는 중심 경로입니다.
- `../internal/wal/wal.go`: record 인코딩과 checksum 검증, replay stopping rule을 확인할 수 있습니다.
- `../tests/wal_test.go`: corruption, truncation, reopen recovery, WAL rotation을 검증합니다.
- `../docs/concepts/wal-record-format.md`: record가 어떤 byte layout으로 저장되는지 먼저 읽어 두면 구현 이해가 빨라집니다.

## 의도적으로 남겨 둔 범위 밖 항목
- group commit, fsync policy, segment compaction 같은 운영 최적화는 다루지 않습니다.
- replication이나 distributed log는 다른 트랙 주제로 남깁니다.

## 데모에서 바로 확인할 장면
- 값을 쓴 뒤 store를 다시 열어 recovery 결과를 출력합니다.
