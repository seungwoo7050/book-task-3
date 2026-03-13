# 20 04 Buffer Pool에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 기능 목록을 다시 적기보다, 규칙이 실제 코드에서 언제 강제되는지 보여 주는 데 초점을 둔다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — Page에서 invariant가 잠기는 지점 보기

이번 세션의 목표는 `Page`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 초기 가설은 `Page` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

막상 다시 펼쳐 보니 `rg -n "Page|Entry" src`로 핵심 함수 위치를 다시 잡고, `Page`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `Page` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`의 `Page`

CLI:

```bash
$ rg -n "Page|Entry" src
src/buffer_pool/core.py:10:class Entry:
src/buffer_pool/core.py:26:    def put(self, key: str, value: object) -> Entry | None:
src/buffer_pool/core.py:34:            evicted = Entry(old_key, old_value)
src/buffer_pool/core.py:53:class Page:
src/buffer_pool/core.py:67:    def fetch_page(self, page_id: str) -> Page:
src/buffer_pool/core.py:71:            assert isinstance(page, Page)
src/buffer_pool/core.py:79:        page = Page(page_id, data, pin_count=1)
src/buffer_pool/core.py:84:            assert isinstance(evicted_page, Page)
src/buffer_pool/core.py:97:        assert isinstance(page, Page)
src/buffer_pool/core.py:108:        assert isinstance(page, Page)
src/buffer_pool/core.py:131:    def _write_page(self, page: Page) -> None:
src/buffer_pool/__init__.py:1:from .core import BufferPool, LRUCache, Page
src/buffer_pool/__init__.py:3:__all__ = ["BufferPool", "LRUCache", "Page"]
```

검증 신호:
- `Page` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `고정 크기 page를 메모리에 캐시하는 기본 구조를 익힙니다.`

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

`Page`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Pin And Dirty`에서 정리한 요점처럼, pin count가 0보다 큰 page는 eviction 대상이 될 수 없다.

다음으로 넘긴 질문:
- `Entry`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — Entry로 같은 규칙 다시 확인하기

이 구간에서 먼저 붙잡으려 한 것은 `Entry`가 `Page`와 어떤 짝을 이루는지 확인하는 것이었다. 처음 읽을 때는 `Entry`는 단순 보조 함수일 거라고 생각했다.

그런데 두 번째 앵커를 읽고 나니, 실제로는 `Page`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `Entry`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`의 `Entry`

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
- `Entry`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_lru_ordering_and_delete` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
class Entry:
    key: str
    value: object


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._items: OrderedDict[str, object] = OrderedDict()
```

왜 여기서 판단이 바뀌었는가:

`Entry`가 없으면 `Page`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Pin And Dirty`에서 정리한 요점처럼, pin count가 0보다 큰 page는 eviction 대상이 될 수 없다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
