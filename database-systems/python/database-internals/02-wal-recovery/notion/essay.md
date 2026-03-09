# WAL Recovery (Python) — 기록하지 않은 것은 존재하지 않는다

## 들어가며

01-mini-lsm-store에서 만든 저장소는 프로세스가 죽으면 memtable의 데이터를 잃는다. 이 프로젝트는 그 약점을 해결한다. **WAL(Write-Ahead Log)**을 도입하여, 모든 쓰기를 memtable에 반영하기 *전에* 디스크에 먼저 기록한다. 프로세스가 죽어도 WAL을 재생하면 마지막 상태까지 복원할 수 있다.

## 바이너리 레코드 포맷

Go 트랙과 동일한 바이너리 포맷을 Python의 `struct` 모듈로 구현한다:

```
[CRC32 4B][Type 1B][KeyLen 4B][ValLen 4B][Key][Value]
```

```python
def _append_record(self, record_type: int, key: str, value: str | None) -> None:
    key_bytes = key.encode()
    value_bytes = b"" if value is None else value.encode()
    value_length = TOMBSTONE_MARKER if value is None else len(value_bytes)
    header = struct.pack(">BII", record_type, len(key_bytes), value_length)
    payload = header + key_bytes + value_bytes
    record = struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF) + payload
    self._handle.write(record)
    self._handle.flush()
```

`TOMBSTONE_MARKER = 0xFFFFFFFF`로 delete를 표현한다. Go 트랙의 `shared/serializer`와 동일한 관례다. `struct.pack(">BII")`는 big-endian으로 1바이트 타입 + 4바이트 키 길이 + 4바이트 값 길이를 패킹한다.

Python의 `zlib.crc32`는 부호가 있을 수 있으므로 `& 0xFFFFFFFF`로 unsigned로 맞춘다.

## Recovery: Stop-on-Corruption

복구의 핵심 원칙은 "첫 번째 손상에서 멈추라"다.

```python
def recover(self) -> list[WALRecord]:
    buffer = self.path.read_bytes()
    while offset < len(buffer):
        if offset + 13 > len(buffer):
            break  # 헤더 불완전
        # ... CRC, type, keyLen, valLen 읽기
        if zlib.crc32(payload) & 0xFFFFFFFF != stored_crc:
            break  # CRC 불일치 → 손상
        # 정상 레코드 추가
```

세 가지 중단 조건:
1. 남은 바이트가 헤더(13B)보다 적음 → partial write
2. 남은 바이트가 전체 레코드보다 적음 → truncated write
3. CRC 불일치 → 데이터 손상

손상 이후 레코드는 *신뢰할 수 없으므로* 모두 버린다. 이것이 "보수적 복구"다.

## DurableStore: LSM + WAL 통합

```python
class DurableStore:
    def put(self, key: str, value: str) -> None:
        self._wal.append_put(key, value)       # 1. WAL에 먼저 기록
        self._replace_memtable_value(key, value) # 2. 그 다음 memtable 반영
        self._maybe_flush()
```

순서가 중요하다. WAL 기록이 실패하면 memtable에 반영하지 않는다. 이것이 **append-before-apply** 원칙이다.

`open()` 시점에 WAL을 recover하여 memtable을 복원한다:

```python
def open(self) -> None:
    # ... SSTable 로드 ...
    for record in WriteAheadLog(self.wal_path, False).recover():
        self._replace_memtable_value(record.key, ...)
    self._wal.open()
```

## WAL Rotation

Flush 후에는 WAL이 더 이상 필요 없다. 데이터가 SSTable에 영속화되었기 때문이다:

```python
def force_flush(self) -> None:
    # ... SSTable 기록 ...
    self._wal.close()
    if self.wal_path.exists():
        self.wal_path.unlink()  # WAL 삭제
    self._wal = WriteAheadLog(self.wal_path, ...)
    self._wal.open()  # 새 WAL 시작
```

rotation 후 WAL 파일 크기가 0이 되는 것을 테스트에서 확인한다.

## 테스트 구성

7개 테스트:

| 테스트 | 검증 내용 |
|--------|----------|
| test_recover_put_records | PUT 2건 → recover 2건 |
| test_recover_delete_records | PUT + DELETE → 타입 구분 확인 |
| test_recover_many_records | 500건 대량 WAL 복구 |
| test_stop_at_corrupted_record | 정상 2건 + 손상 바이트 → 2건만 복구 |
| test_recover_nonexistent_and_truncated | 미존재/절단 파일 → 빈 리스트 |
| test_store_recovers_from_wal_after_reopen | close → reopen → WAL에서 복구 |
| test_force_flush_rotates_wal | flush 후 WAL 크기 0, SSTable에서 값 유지 |

## 돌아보며

이 프로젝트는 Go 트랙 04-wal-recovery의 Python 포트이지만, `struct`와 `zlib`라는 Python 표준 라이브러리로 바이너리 포맷을 다루는 경험을 제공한다. WAL의 핵심—append-before-apply, CRC 검증, stop-on-corruption—은 언어에 상관없이 동일하다.
