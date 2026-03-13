# 20 recover 는 어디서 멈추는가

## Day 1
### Session 3

`recover()`를 읽을 때 가장 먼저 본 조건은 아래 두 줄이었다.

```python
if offset + record_size > len(buffer):
    break
if zlib.crc32(payload) & 0xFFFFFFFF != stored_crc:
    break
```

중요한 점은 `continue`가 아니라 `break`라는 것이다. 파일 끝부분이 잘렸거나 CRC가 맞지 않으면 그 지점 이후는 전부 신뢰하지 않는다. `test_stop_at_corrupted_record`가 정확히 이 동작을 계약으로 고정한다.

- 목표: truncated/corrupted tail 처리 정책을 코드와 테스트에서 교차 확인
- 진행: `WriteAheadLog.recover`와 `test_stop_at_corrupted_record`, `test_recover_nonexistent_and_truncated` 대조
- 판단: 이 구현은 "최대한 많이 복구"보다 "신뢰 가능한 구간까지만 복구"를 선택

CLI:

```bash
cd python/database-internals/projects/02-wal-recovery
sed -n '1,220p' src/wal_recovery/store.py
sed -n '1,120p' tests/test_wal_recovery.py
```

### Session 4

flush 경계도 같이 봤다. `force_flush()`는 단순히 memtable을 SSTable로 내리는 함수가 아니었다.

```python
self._wal.close()
if self.wal_path.exists():
    self.wal_path.unlink()
self.memtable.clear()
self._wal = WriteAheadLog(self.wal_path, self._wal.fsync_enabled)
self._wal.open()
```

WAL을 닫고 삭제한 뒤 `active.wal`을 새로 연다. 즉 flush 이전 write는 SSTable로 내려가고, flush 이후 write만 새 WAL에 쌓인다. `test_force_flush_rotates_wal`에서 `active.wal` 크기가 0으로 검증되는 이유가 여기 있다.

이 단계에서 재정리한 핵심:

- `append -> memtable apply` 순서가 durability 기준선
- recover는 "첫 손상 지점에서 중단"이 안전 기준선
- flush는 `SSTable 생성 + WAL 회전`까지 포함해야 replay 윈도우가 줄어든다

다음 질문:

- SSTable 개수가 늘어날 때 WAL 복구 뒤 read path 비용은 어떻게 변하나
- index/filter를 붙이면 recovery 이후 point lookup 비용은 얼마나 줄어드나