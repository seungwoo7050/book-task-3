# 지식 인덱스

## 핵심 용어
- `WAL`: write-ahead log로, memory update 전에 durable append를 남기는 로그입니다.
- `replay`: 재시작 후 WAL record를 다시 적용해 메모리 상태를 복원하는 과정입니다.
- `checksum`: record가 손상되었는지 판단하는 무결성 값입니다.
- `rotation`: flush 후 새 active WAL 파일로 넘어가는 동작입니다.
- `truncated record`: 길이가 모자라 끝까지 읽을 수 없는 미완성 record입니다.

## 다시 볼 파일
- `../src/wal_recovery/store.py`: `DurableStore`가 WAL, memtable, flush를 함께 묶는 중심 경로입니다.
- `../src/wal_recovery/store.py`: record 인코딩과 checksum 검증, replay stopping rule을 확인할 수 있습니다.
- `../tests/test_wal_recovery.py`: corruption, truncation, reopen recovery, WAL rotation을 검증합니다.
- `../docs/concepts/wal-record-format.md`: record가 어떤 byte layout으로 저장되는지 먼저 읽어 두면 구현 이해가 빨라집니다.

## 개념 문서
- `../docs/concepts/recovery-policy.md`: 손상된 WAL을 어디까지 신뢰하고 어느 지점에서 멈출지 설명합니다.
- `../docs/concepts/wal-record-format.md`: record 인코딩과 checksum, 길이 정보가 복구에 어떤 역할을 하는지 정리합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/test_wal_recovery.py`
- 다시 돌릴 테스트 이름: `test_recover_put_records`, `test_recover_delete_records`, `test_recover_many_records`, `test_stop_at_corrupted_record`, `test_recover_nonexistent_and_truncated`, `test_store_recovers_from_wal_after_reopen`, `test_force_flush_rotates_wal`
- 데모 경로: `../src/wal_recovery/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 `name`, `city`를 쓴 뒤 store를 닫고 다시 열어 복원된 값을 출력합니다. Python 데모도 같은 복구 장면을 JSON 형태로 보여 줍니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
