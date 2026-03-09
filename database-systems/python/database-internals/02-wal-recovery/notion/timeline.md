# 02-wal-recovery 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p python/database-internals/02-wal-recovery
cd python/database-internals/02-wal-recovery
mkdir -p src/wal_recovery tests docs/concepts docs/references problem
touch src/wal_recovery/__init__.py src/wal_recovery/__main__.py
```

### pyproject.toml
```toml
[project]
name = "wal-recovery"
requires-python = ">=3.14"
```

```bash
python3 -m pip install -U pytest
```

## Phase 1 — WAL 레코드 포맷 구현

파일: `src/wal_recovery/store.py`

### 상수 정의
```python
TOMBSTONE_MARKER = 0xFFFFFFFF
OP_PUT = 0x01
OP_DELETE = 0x02
```

### WALRecord dataclass
```python
@dataclass(slots=True)
class WALRecord:
    record_type: str  # "put" | "delete"
    key: str
    value: str | None = None
```

### WriteAheadLog 클래스
- `open()`: `Path.open("ab")` — binary append 모드
- `append_put/append_delete`: `_append_record` 호출
- `_append_record`: `struct.pack(">BII")` + `zlib.crc32` + write + flush
- `recover()`: 바이너리 파싱, 3가지 중단 조건 (헤더 부족/레코드 부족/CRC 불일치)
- `close()`: 파일 핸들 정리

## Phase 2 — SSTable 복사

01-mini-lsm-store의 SSTable 클래스를 이 파일에 복사. JSON Lines 포맷 동일.

## Phase 3 — DurableStore 구현

- `open()`: SSTable 로드 + WAL recover → memtable 복원 + WAL open
- `put(key, value)`: WAL append → memtable 반영 → maybe_flush (append-before-apply)
- `delete(key)`: WAL append → memtable 반영
- `get(key)`: memtable → SSTable (newest first)
- `force_flush()`: SSTable 기록 → WAL close + unlink + 재생성 (rotation)
- `close()`: WAL close (flush 없이 — memtable은 WAL에서 복구 가능)

## Phase 4 — 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

7개 테스트: put/delete recover, 500건 대량, corruption stop, truncated, reopen 복구, flush rotation.

## Phase 5 — 데모

```bash
PYTHONPATH=src python3 -m wal_recovery
```

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 코드 | ~190줄 |
| 테스트 케이스 | 7개 |
| 외부 의존성 | pytest |
| 핵심 클래스 | WriteAheadLog, DurableStore, SSTable |

## Go 트랙 대응

| Python 02 | Go 트랙 |
|-----------|---------|
| WriteAheadLog | 04-wal-recovery/internal/wal |
| DurableStore | 04-wal-recovery/internal/store |
| zlib.crc32 | shared/hash.CRC32 |
| struct.pack | shared/serializer |
