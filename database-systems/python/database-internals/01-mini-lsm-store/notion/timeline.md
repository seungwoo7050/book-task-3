# 01-mini-lsm-store 개발 타임라인

## Phase 0 — 프로젝트 초기화

```bash
mkdir -p python/database-internals/01-mini-lsm-store
cd python/database-internals/01-mini-lsm-store
```

Python 프로젝트 구조 생성:
```bash
mkdir -p src/mini_lsm_store
mkdir -p tests
mkdir -p docs/concepts docs/references
mkdir -p problem/code problem/data problem/script
touch src/mini_lsm_store/__init__.py
touch src/mini_lsm_store/__main__.py
```

### pyproject.toml 설정
```toml
[project]
name = "mini-lsm-store"
version = "0.1.0"
requires-python = ">=3.14"
```

### 의존성 설치
```bash
python3 -m pip install -U pytest
```

Go 트랙과 달리 빌드 시스템이 없다. `PYTHONPATH=src`로 소스 경로를 지정하여 실행.

## Phase 1 — 문제 정의

### 1-1. problem/README.md
- Go 트랙의 01(SkipList), 02(SSTable), 03(LSM Store)를 한 프로젝트로 압축
- Python dict → memtable, JSON Lines → SSTable

### 1-2. docs/concepts/
- `flush-lifecycle.md`: active → immutable → SSTable → registry
- `read-path.md`: active → immutable → newest SSTable → oldest SSTable

## Phase 2 — SSTable 클래스 구현

파일: `src/mini_lsm_store/store.py`

### 2-1. SSTable dataclass
```python
@dataclass(slots=True)
class SSTable:
    path: Path
    index: dict[str, str | None] | None = None
```
- `slots=True`: 메모리 최적화
- `index`: lazy loading (None → load 시 dict)

### 2-2. file_name 클래스 메서드
```python
@classmethod
def file_name(cls, data_dir: Path, sequence: int) -> Path:
    return data_dir / f"{sequence:06d}.sst"
```
- 6자리 zero-padded 시퀀스 → 파일명 정렬 가능

### 2-3. write / load / get
- `write`: `json.dumps` + newline → JSON Lines 포맷
- `load`: 파일 읽기 → dict 구성
- `get`: lazy load + dict lookup → `(value, found)` 반환

## Phase 3 — MiniLSMStore 구현

### 3-1. __init__
```python
def __init__(self, data_dir, memtable_size_threshold=64*1024):
```
- `data_dir`: SSTable 저장 디렉터리
- `memtable_size_threshold`: 자동 flush 임계값 (기본 64KB)
- `_byte_size`: memtable 바이트 크기 추적
- `_next_sequence`: SSTable 파일명 시퀀스

### 3-2. open
- `data_dir` 디렉터리 생성 (`mkdir(parents=True, exist_ok=True)`)
- `glob("*.sst")` → 파일 정렬 후 SSTable 로드
- `reverse()` → newest-first 순서
- 최대 시퀀스 번호 + 1 → `_next_sequence`

### 3-3. put / delete
- `put(key, value)` → `_replace_memtable_value(key, value)` + `_maybe_flush()`
- `delete(key)` → `_replace_memtable_value(key, None)` (tombstone)

### 3-4. _replace_memtable_value (바이트 크기 추적)
- 이전 값 존재 시: 이전 크기 차감
- 새 값 크기 추가
- `...` (Ellipsis)를 "키 미존재" 센티널로 사용 — `None`과 구분

### 3-5. get (newest-first 읽기 경로)
1. `key in self.memtable` → 반환
2. `key in self.immutable_memtable` → 반환
3. `for table in self.sstables` (newest first) → `table.get(key)` → found 시 반환
4. 모두 없으면 `(None, False)`

### 3-6. force_flush
1. `dict(self.memtable)` → immutable 복사
2. `self.memtable.clear()` + `_byte_size = 0`
3. `sorted()` → 키 정렬된 레코드
4. SSTable.write(records)
5. `self.sstables.insert(0, table)` → newest first
6. `self.immutable_memtable = None`

### 3-7. close
- `force_flush()` 호출 — memtable 잔여 데이터 디스크 기록

### 3-8. _maybe_flush
- `_byte_size >= threshold` → `force_flush()`

## Phase 4 — __main__.py 데모

```python
# src/mini_lsm_store/__main__.py
from mini_lsm_store.store import demo
demo()
```

실행:
```bash
PYTHONPATH=src python3 -m mini_lsm_store
```

## Phase 5 — __init__.py 모듈 설정

```python
# src/mini_lsm_store/__init__.py
from mini_lsm_store.store import MiniLSMStore
```
- 테스트에서 `from mini_lsm_store import MiniLSMStore` 사용 가능

## Phase 6 — 테스트 작성

파일: `tests/test_mini_lsm_store.py`

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

| 테스트 | 검증 내용 |
|--------|----------|
| test_put_and_get | 기본 put/get |
| test_missing_key | 없는 키 (None, False) |
| test_update | 값 덮어쓰기 |
| test_delete | tombstone (None, True) |
| test_flush_creates_sstable | 자동 flush 발생 확인 |
| test_read_after_force_flush | flush 후 읽기 |
| test_memtable_wins_over_sstable | memtable 우선순위 |
| test_tombstone_across_levels | cross-level tombstone |
| test_persistence_after_reopen | close → reopen 영속성 |

`open_store` 헬퍼: `tmp_path` fixture 사용 (pytest 자동 임시 디렉터리).

## 구현 통계

| 항목 | 수치 |
|------|------|
| 소스 파일 | 1개 (store.py) |
| 소스 코드 | ~110줄 |
| 테스트 파일 | 1개 |
| 테스트 케이스 | 9개 |
| 외부 의존성 | pytest (테스트만) |
| Python 버전 | 3.14 |

## Go 트랙과의 대응

| Python 01 | Go 트랙 |
|-----------|---------|
| dict memtable | 01-memtable-skiplist (SkipList) |
| JSON Lines SSTable | 02-sstable-format (바이너리) |
| MiniLSMStore | 03-mini-lsm-store |
| tombstone=None | TombstoneMarker=0xFFFFFFFF |
