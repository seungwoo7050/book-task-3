# 04 Buffer Pool — 개발 타임라인

## Phase 0: 환경 준비

```bash
cd python/database-internals/04-buffer-pool
python3 --version
# Python 3.14.x

python3 -m pip install -U pytest
```

### 디렉토리 구조 생성

```bash
mkdir -p src/buffer_pool tests docs/concepts docs/references
touch src/buffer_pool/__init__.py
touch src/buffer_pool/__main__.py
touch src/buffer_pool/core.py
touch tests/test_buffer_pool.py
```

---

## Phase 1: LRU Cache 구현

### 1.1 Entry dataclass

```python
@dataclass(slots=True)
class Entry:
    key: str
    value: object
```

eviction 시 caller에게 축출된 항목을 알려주기 위한 래퍼.

### 1.2 OrderedDict 기반 LRU

**결정**: Go 버전처럼 DoublyLinkedList를 직접 구현하지 않고 `collections.OrderedDict`를 사용. Python stdlib이 이미 O(1) 순서 변경을 지원하기 때문.

핵심 API:
- `move_to_end(key, last=False)` → MRU(앞)로 이동
- `popitem(last=True)` → LRU(뒤)에서 제거

```python
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._items: OrderedDict[str, object] = OrderedDict()
```

### 1.3 LRU 단독 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_buffer_pool.py::test_lru_basic_operations -v
PYTHONPATH=src python3 -m pytest tests/test_buffer_pool.py::test_lru_eviction_and_promotion -v
PYTHONPATH=src python3 -m pytest tests/test_buffer_pool.py::test_lru_ordering_and_delete -v
```

3개 테스트로 기본 동작, eviction 순서, 삭제를 검증.

---

## Phase 2: Page와 parse_page_id

### 2.1 Page dataclass

```python
@dataclass(slots=True)
class Page:
    page_id: str     # "파일경로:페이지번호"
    data: bytearray  # 고정 크기 페이지 데이터
    dirty: bool = False
    pin_count: int = 0
```

**결정**: `data`를 `bytes`가 아닌 `bytearray`로. in-place 수정이 필요하기 때문.

### 2.2 page_id 파싱

```python
def parse_page_id(page_id: str) -> tuple[str, int]:
    file_path, page_number = page_id.rsplit(":", 1)
    return str(Path(file_path)), int(page_number)
```

**결정**: `rsplit(":", 1)` 사용. 파일 경로에 `:`가 포함될 수 있으므로 마지막 콜론만 분리.

---

## Phase 3: BufferPool 구현

### 3.1 기본 구조

```python
class BufferPool:
    def __init__(self, max_pages: int, page_size: int = 4096) -> None:
        self.max_pages = max_pages
        self.page_size = page_size or 4096
        self.cache = LRUCache(max_pages)
        self.file_handles: dict[str, object] = {}
```

### 3.2 fetch_page 구현

두 경로:
1. **캐시 히트**: `cache.get()` 성공 → pin_count 증가 → 같은 Page 반환
2. **캐시 미스**: 파일에서 `seek` + `read` → 새 Page 생성 → cache에 put

eviction 발생 시:
- pinned page면 다시 캐시에 넣고 RuntimeError
- dirty page면 `_write_page()` 호출

### 3.3 fetch 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_buffer_pool.py::test_fetch_page_from_disk -v
PYTHONPATH=src python3 -m pytest tests/test_buffer_pool.py::test_return_cached_page -v
```

`test_return_cached_page`는 `page1 is page2`로 동일 객체 반환을 확인.

### 3.4 unpin_page 구현

```python
def unpin_page(self, page_id: str, is_dirty: bool) -> None:
```

- pin_count 감소
- `is_dirty=True`면 dirty flag 설정

### 3.5 flush_page / flush_all

```python
def _write_page(self, page: Page) -> None:
    handle.seek(page_number * self.page_size)
    handle.write(page.data)
    handle.flush()
```

### 3.6 dirty 추적 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_buffer_pool.py::test_track_dirty_pages -v
```

### 3.7 eviction 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_buffer_pool.py::test_eviction_after_unpin -v
```

max_pages=2인 pool에서 3개 페이지를 순차 fetch. 각각 unpin 후 eviction이 정상 동작하는지 확인.

---

## Phase 4: 파일 핸들 관리

### 4.1 핸들 캐싱

```python
def _get_handle(self, file_path: str):
    handle = self.file_handles.get(file_path)
    if handle is None:
        handle = Path(file_path).open("r+b")
        self.file_handles[file_path] = handle
    return handle
```

**결정**: `"r+b"` 모드로 읽기+쓰기 모두 하나의 핸들로 처리.

### 4.2 close

```python
def close(self) -> None:
    self.flush_all()
    for handle in self.file_handles.values():
        handle.close()
    self.file_handles.clear()
```

`close()` 전에 `flush_all()`로 dirty page 보장.

---

## Phase 5: Demo와 마무리

### 5.1 seed_pages 헬퍼 (테스트)

```python
def seed_pages(tmp_path) -> Path:
    data_file = Path(tmp_path) / "data.db"
    pages = bytearray()
    for index in range(10):
        buffer = bytearray(64)
        payload = f"page-{index}".encode()
        buffer[: len(payload)] = payload
        pages.extend(buffer)
    data_file.write_bytes(pages)
    return data_file
```

10개 64바이트 페이지를 미리 생성. 모든 buffer pool 테스트의 fixture.

### 5.2 demo 실행

```bash
PYTHONPATH=src python3 -m buffer_pool
# {"page_id": "...:0", "pin_count": 1, "prefix": "page-0"}
```

### 5.3 전체 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

7개 테스트 모두 통과 확인.

---

## Phase 6: 개념 문서 작성

### docs/concepts/lru-eviction.md
- doubly-linked list + hash map = O(1) LRU
- Python에서는 OrderedDict가 이 역할

### docs/concepts/pin-and-dirty.md
- pin count > 0이면 eviction 불가
- dirty page는 eviction 전 반드시 write-back

---

## 소스코드에서 드러나지 않는 결정들

1. **OrderedDict 선택**: Go에서 100줄 이상의 linked list 코드가 Python에서는 stdlib 한 줄로 대체. 학습 목적과 구현 효율 사이의 트레이드오프.

2. **page_size 기본값 4096**: 실제 OS 페이지 크기와 동일. 테스트에서는 64바이트 사용하여 빠르게 검증.

3. **파일 핸들 캐싱**: 매번 open/close 하지 않고 dict에 보관. 같은 파일의 다른 페이지를 seek만으로 접근 가능.

4. **pinned page eviction 시 복원**: evicted page를 다시 cache에 넣은 후 RuntimeError. 데이터 손실 방지가 에러보다 우선.

5. **`r+b` 모드**: read-only나 write-only가 아닌 read+write binary. 하나의 핸들로 fetch와 flush를 모두 처리.

6. **`slots=True` 일관 사용**: Entry, Page 모두 `slots=True`로 메모리 효율 최적화. `__dict__` 생성 방지.
