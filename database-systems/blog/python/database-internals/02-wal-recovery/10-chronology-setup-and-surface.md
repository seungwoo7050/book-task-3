# 10 WAL 을 붙이면 무엇이 달라지는가

## Day 1
### Session 1

`01-mini-lsm-store`에서 가장 불안했던 지점은 하나였다. memtable에 먼저 반영하고 flush 전에 프로세스가 죽으면, 그 write는 그냥 사라진다. 이 프로젝트를 열자마자 `store.py` 상단에 아래 상수들이 먼저 보였다.

```python
TOMBSTONE_MARKER = 0xFFFFFFFF
OP_PUT = 0x01
OP_DELETE = 0x02
```

처음엔 "WAL 포맷 구현 연습" 정도로 봤는데, 테스트 이름이 생각을 바꿨다.

```bash
cd python/database-internals/projects/02-wal-recovery
grep -n "def test_" tests/test_wal_recovery.py
```

```text
6:def test_recover_put_records(tmp_path):
36:def test_stop_at_corrupted_record(tmp_path):
53:def test_store_recovers_from_wal_after_reopen(tmp_path):
60:def test_force_flush_rotates_wal(tmp_path):
```

핵심은 포맷이 아니라 recovery 경계였다. "어디까지 replay를 신뢰할 수 있나"를 테스트로 고정해 둔 구조다.

- 목표: append-before-apply 순서가 실제로 지켜지는지 확인한다
- 진행: `DurableStore.put/delete`, `WriteAheadLog._append_record/recover`를 먼저 읽었다
- 이슈: 처음엔 `put`이 memtable 갱신 후 WAL append라고 예상했지만 반대였다

```python
def put(self, key: str, value: str) -> None:
    self._wal.append_put(key, value)
    self._replace_memtable_value(key, value)
    self._maybe_flush()
```

이 순서가 이 프로젝트 전체를 설명한다. 장애 시 복구는 memtable이 아니라 WAL을 기준으로 한다.

### Session 2

레코드 wire format도 코드에서 바로 드러난다.

```python
header = struct.pack(">BII", record_type, len(key_bytes), value_length)
payload = header + key_bytes + value_bytes
record = struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF) + payload
```

`[crc32][type][key_len][value_len][key][value]` 구조고, delete는 `value_len = TOMBSTONE_MARKER`로 인코딩된다. 이 tombstone 규칙은 01의 `None` 삭제 semantics를 바이너리 로그 포맷으로 내린 버전이다.

당시에는 체크섬 계산보다 recover 중단 정책이 더 중요해 보였다. 손상 레코드를 건너뛰는 게 아니라 "첫 불신 지점에서 중단"하는 정책이라서, 뒷부분 garbage를 진짜 로그로 오인하지 않는다.

- 판단: 이 프로젝트의 학습 포인트는 `WAL bytes`가 아니라 `recovery boundary`다
- 다음 질문: flush 시점에 WAL 파일을 어떻게 회전시켜 replay 범위를 줄이는가