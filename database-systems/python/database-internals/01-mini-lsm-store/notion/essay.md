# Mini LSM Store (Python) — 하나의 파일에 담은 저장 엔진

## 들어가며

Python database-internals 시리즈의 첫 프로젝트다. Go 트랙에서는 SkipList(01), SSTable(02), LSM Store(03)를 세 개의 독립 프로젝트로 나눴지만, Python 트랙은 진입 비용을 낮추기 위해 이 세 가지를 **하나로 접는다**.

결과물은 `store.py` 한 파일, 약 110줄. 이 안에 in-memory memtable, immutable swap, SSTable flush, newest-first read, tombstone, reopen이 모두 들어 있다.

## Go 트랙과의 차이

Go 트랙의 memtable은 SkipList라는 확률적 자료구조를 직접 구현했다. Python 트랙은 `dict`를 사용한다. 정렬 순서가 필요 없는 단순 KV 접근에서 `dict`는 O(1) 해시맵이므로 더 자연스러운 선택이다. SSTable로 flush할 때 `sorted()`로 정렬하면 된다.

SSTable 포맷도 다르다. Go는 바이너리(길이 접두사 + 바이트 직렬화)였지만, Python은 **JSON Lines** — 한 줄에 하나의 JSON 객체. 사람이 읽을 수 있고, 디버깅이 쉽다.

## SSTable 클래스

```python
@dataclass(slots=True)
class SSTable:
    path: Path
    index: dict[str, str | None] | None = None
```

`slots=True`는 Python 3.10+의 최적화 — `__dict__` 대신 고정 슬롯으로 메모리를 절약한다.

`write` 메서드는 `(key, value)` 튜플 리스트를 받아 JSON Lines로 기록한다. `load`는 파일을 읽어 인메모리 `index` dict를 채운다. `get`은 lazy loading — 처음 조회 시 `load`가 자동 호출된다.

```python
def get(self, key: str) -> tuple[str | None, bool]:
    if self.index is None:
        self.load()
    if key not in self.index:
        return None, False
    return self.index[key], True
```

반환 타입 `(value, found)` 패턴은 Go의 `(value, ok)` 관용구를 Python에 그대로 가져온 것이다.

## MiniLSMStore: 핵심 동작

### 쓰기

```python
def put(self, key: str, value: str) -> None:
    self._replace_memtable_value(key, value)
    self._maybe_flush()
```

`_replace_memtable_value`는 바이트 크기를 정확히 추적한다. 이전 값이 있으면 그 크기를 빼고, 새 값의 크기를 더한다. 이 추적이 threshold 기반 자동 flush를 가능하게 한다.

### 삭제

```python
def delete(self, key: str) -> None:
    self._replace_memtable_value(key, None)
```

`None`이 tombstone이다. Go 트랙에서는 `TombstoneMarker(0xFFFFFFFF)` 같은 센티널 값을 썼지만, Python에서는 `None`이 자연스럽다.

### 읽기 경로 (Newest-First)

```python
def get(self, key: str) -> tuple[str | None, bool]:
    if key in self.memtable:
        return self.memtable[key], True
    if self.immutable_memtable is not None and key in self.immutable_memtable:
        return self.immutable_memtable[key], True
    for table in self.sstables:  # newest first
        value, found = table.get(key)
        if found:
            return value, True
    return None, False
```

1. Active memtable → 2. Immutable memtable → 3. SSTable (newest first). 먼저 찾으면 즉시 반환. tombstone(`None`)도 "찾았다"로 간주하여 이전 SSTable의 값을 가리는 역할을 한다.

### Flush

```python
def force_flush(self) -> None:
    self.immutable_memtable = dict(self.memtable)
    self.memtable.clear()
    self._byte_size = 0
    records = sorted(self.immutable_memtable.items())
    table = SSTable(SSTable.file_name(self.data_dir, self._next_sequence))
    table.write(records)
    self.sstables.insert(0, table)
    self.immutable_memtable = None
```

핵심 순서:
1. active → immutable 복사 후 active 비움 (새 쓰기를 즉시 받을 수 있도록)
2. 정렬 후 SSTable 기록
3. SSTable 리스트 맨 앞에 삽입 (newest first)
4. immutable 해제

### Reopen

`open()` 메서드는 data 디렉터리의 `.sst` 파일을 정렬 후 로드한다. `reverse()`로 newest-first 순서를 만든다. 파일명의 시퀀스 번호로 다음 번호를 결정한다.

## 테스트 구성

8개 테스트가 LSM 스토어의 핵심 동작을 검증한다:

| 테스트 | 검증 내용 |
|--------|----------|
| test_put_and_get | 기본 put → get |
| test_missing_key | 없는 키 → (None, False) |
| test_update | 같은 키 덮어쓰기 |
| test_delete | delete 후 (None, True) — tombstone |
| test_flush_creates_sstable | threshold 초과 시 자동 flush |
| test_read_after_force_flush | flush 후에도 읽기 가능 |
| test_memtable_wins_over_sstable | memtable 값이 SSTable보다 우선 |
| test_tombstone_across_levels | flush 후 delete → SSTable 값 가려짐 |
| test_persistence_after_reopen | close → reopen → 값 유지 |

## 돌아보며

Go 트랙의 세 프로젝트를 하나로 압축했지만, 핵심 개념은 모두 살아 있다. memtable → immutable swap → SSTable flush 라이프사이클, newest-first 읽기, tombstone의 cross-level 삭제 의미. Python의 `dict`와 JSON Lines가 구현을 훨씬 간결하게 만들어, LSM 트리의 **아키텍처**에 집중할 수 있다.
