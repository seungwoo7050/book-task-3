# 10 04 Buffer Pool를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 설명문을 믿고 곧장 구현으로 들어가기보다, 테스트와 파일 구조를 다시 읽으면서 어디서부터 이야기를 시작해야 하는지 정리한다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

여기서 가장 먼저 확인한 것은 `04 Buffer Pool`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다. 처음에는 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

하지만 실제로는 `find src tests -type f | sort`로 구조를 펼친 뒤 `rg -n "^def test_" tests`로 테스트 이름을 나열했다. `test_lru_ordering_and_delete`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `Page` 주변의 invariant를 고정하는 일이라는 게 보였다. 결정적으로 방향을 잡아 준 신호는 `test_lru_basic_operations`는 가장 기본 표면을 보여 줬고, `test_lru_ordering_and_delete`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/python/database-internals/projects/04-buffer-pool/README.md`, `database-systems/python/database-internals/projects/04-buffer-pool/tests/test_buffer_pool.py`

CLI:

```bash
$ find src tests -type f | sort
src/buffer_pool/__init__.py
src/buffer_pool/__main__.py
src/buffer_pool/__pycache__/__init__.cpython-312.pyc
src/buffer_pool/__pycache__/__init__.cpython-314.pyc
src/buffer_pool/__pycache__/__main__.cpython-312.pyc
src/buffer_pool/__pycache__/__main__.cpython-314.pyc
src/buffer_pool/__pycache__/core.cpython-312.pyc
src/buffer_pool/__pycache__/core.cpython-314.pyc
src/buffer_pool/core.py
tests/__pycache__/test_buffer_pool.cpython-312-pytest-8.3.5.pyc
tests/__pycache__/test_buffer_pool.cpython-312-pytest-9.0.2.pyc
tests/__pycache__/test_buffer_pool.cpython-314-pytest-9.0.2.pyc
tests/test_buffer_pool.py
```

```bash
$ rg -n "^def test_" tests
tests/test_buffer_pool.py:6:def test_lru_basic_operations():
tests/test_buffer_pool.py:16:def test_lru_eviction_and_promotion():
tests/test_buffer_pool.py:30:def test_lru_ordering_and_delete():
tests/test_buffer_pool.py:42:def test_fetch_page_from_disk(tmp_path):
tests/test_buffer_pool.py:50:def test_return_cached_page(tmp_path):
tests/test_buffer_pool.py:59:def test_track_dirty_pages(tmp_path):
tests/test_buffer_pool.py:68:def test_eviction_after_unpin(tmp_path):
```

검증 신호:
- `test_lru_basic_operations`는 가장 기본 표면을 보여 줬고, `test_lru_ordering_and_delete`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `Page` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```python
def test_lru_ordering_and_delete():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.keys() == ["c", "b", "a"]
    cache.get("a")
    assert cache.keys() == ["a", "c", "b"]
    assert cache.delete("a") is True
    assert cache.delete("missing") is False
```

왜 여기서 판단이 바뀌었는가:

`test_lru_ordering_and_delete`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `LRU Eviction`에서 정리한 요점처럼, doubly-linked list와 hash map을 조합하면 O(1) get/put/evict가 가능하다.

다음으로 넘긴 질문:
- `Page`와 `Entry`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이번 세션의 목표는 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 초기 가설은 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

막상 다시 펼쳐 보니 가장 큰 구현 파일인 `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `Page` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`

CLI:

```bash
$ rg -n "^(class|def) " src
src/buffer_pool/core.py:10:class Entry:
src/buffer_pool/core.py:15:class LRUCache:
src/buffer_pool/core.py:53:class Page:
src/buffer_pool/core.py:60:class BufferPool:
src/buffer_pool/core.py:139:def parse_page_id(page_id: str) -> tuple[str, int]:
src/buffer_pool/core.py:146:def demo() -> None:
```

검증 신호:
- `Page` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Entry`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```python
class Page:
    page_id: str
    data: bytearray
    dirty: bool = False
    pin_count: int = 0


class BufferPool:
    def __init__(self, max_pages: int, page_size: int = 4096) -> None:
        self.max_pages = max_pages
        self.page_size = page_size or 4096
        self.cache = LRUCache(max_pages)
        self.file_handles: dict[str, object] = {}
```

왜 여기서 판단이 바뀌었는가:

`Page`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Pin And Dirty`에서 정리한 요점처럼, pin count가 0보다 큰 page는 eviction 대상이 될 수 없다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `Entry`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
