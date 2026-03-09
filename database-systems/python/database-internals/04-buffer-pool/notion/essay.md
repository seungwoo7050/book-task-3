# "디스크를 매번 읽지 않는 법" — Python으로 Buffer Pool 만들기

## 문제의 시작

03-index-filter에서 SSTable 조회를 최적화했지만, 같은 블록을 반복해서 읽을 때는 여전히 매번 디스크에 접근한다. 데이터베이스는 이 문제를 **buffer pool**로 해결한다. 고정 크기 페이지를 메모리에 올려놓고, 같은 페이지가 다시 필요하면 디스크를 건드리지 않는다.

이 프로젝트의 핵심 질문: "제한된 메모리에서 어떤 페이지를 남기고 어떤 페이지를 버릴 것인가?"

## LRU Cache: OrderedDict의 힘

Go 버전에서는 HashMap과 DoublyLinkedList를 직접 만들어 O(1) LRU를 구현했다. Python에서는 `collections.OrderedDict`가 이미 그 역할을 한다.

```python
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self._items: OrderedDict[str, object] = OrderedDict()
```

### get: 접근하면 앞으로

```python
def get(self, key: str) -> object | None:
    if key not in self._items:
        return None
    self._items.move_to_end(key, last=False)
    return self._items[key]
```

`move_to_end(key, last=False)`가 핵심이다. `last=False`는 리스트의 **앞쪽(MRU)**으로 이동시킨다. 접근할 때마다 앞으로 보내면, 뒤에 남는 것이 자연스럽게 LRU가 된다.

### put: 가득 차면 뒤에서 꺼내기

```python
def put(self, key: str, value: object) -> Entry | None:
    if key in self._items:
        self._items[key] = value
        self._items.move_to_end(key, last=False)
        return None
    evicted = None
    if len(self._items) >= self.capacity:
        old_key, old_value = self._items.popitem(last=True)
        evicted = Entry(old_key, old_value)
    self._items[key] = value
    self._items.move_to_end(key, last=False)
    return evicted
```

`popitem(last=True)`이 **뒤쪽(LRU)** 항목을 꺼낸다. 꺼낸 항목은 `Entry` dataclass로 반환하여 caller가 후처리(dirty write-back 등)를 할 수 있게 한다.

이 두 메서드가 Go에서 수십 줄의 linked list 조작을 대체한다. Python의 `OrderedDict`가 내부적으로 doubly-linked list를 유지하기 때문이다.

## Page: 고정 크기의 메모리 단위

```python
@dataclass(slots=True)
class Page:
    page_id: str
    data: bytearray
    dirty: bool = False
    pin_count: int = 0
```

네 개의 필드가 각각 의미를 가진다:

- **page_id**: `"파일경로:페이지번호"` 형식. `parse_page_id()`로 분리한다.
- **data**: `bytearray`로 된 고정 크기 블록. 읽기와 쓰기가 모두 가능.
- **dirty**: caller가 data를 수정했는지 여부. `unpin_page(page_id, is_dirty=True)` 호출로 설정.
- **pin_count**: 이 페이지를 사용 중인 caller 수. 0보다 크면 eviction 불가.

### page_id 파싱

```python
def parse_page_id(page_id: str) -> tuple[str, int]:
    if ":" not in page_id:
        raise ValueError("bufferpool: invalid page id")
    file_path, page_number = page_id.rsplit(":", 1)
    return str(Path(file_path)), int(page_number)
```

`rsplit(":", 1)`을 사용하는 이유: 파일 경로에 콜론이 포함될 수 있기 때문에 **맨 마지막 콜론만** 분리한다.

## BufferPool: 모든 것이 합쳐지는 곳

### fetch_page: 캐시 히트와 미스

```python
def fetch_page(self, page_id: str) -> Page:
    cached = self.cache.get(page_id)
    if cached is not None:
        page.pin_count += 1
        return page
    # cache miss → disk read
    file_path, page_number = parse_page_id(page_id)
    handle = self._get_handle(file_path)
    handle.seek(page_number * self.page_size)
    data = bytearray(handle.read(self.page_size))
    page = Page(page_id, data, pin_count=1)
    evicted = self.cache.put(page_id, page)
```

캐시 히트면 pin_count만 올리고 같은 Page 객체를 반환한다. 테스트에서 `page1 is page2`로 동일 객체임을 확인한다.

캐시 미스면 디스크에서 페이지 크기만큼 읽고, 새 Page를 LRU 캐시에 넣는다. 이때 eviction이 발생할 수 있다.

### eviction과 pinned page 보호

```python
if evicted is not None:
    evicted_page = evicted.value
    if evicted_page.pin_count > 0:
        self.cache.put(evicted.key, evicted_page)
        raise RuntimeError("bufferpool: cannot evict pinned page")
    if evicted_page.dirty:
        self._write_page(evicted_page)
```

eviction 대상이 pinned 상태면 **다시 캐시에 넣고 에러를 발생**시킨다. 이것이 buffer pool의 핵심 안전장치다. dirty page는 디스크에 써야만 메모리에서 제거할 수 있다.

### unpin과 dirty 마킹

```python
def unpin_page(self, page_id: str, is_dirty: bool) -> None:
    # ...
    if page.pin_count > 0:
        page.pin_count -= 1
    if is_dirty:
        page.dirty = True
```

caller가 "이 페이지를 수정했다"는 신호는 `is_dirty=True`로 전달한다. dirty flag는 한번 True가 되면 flush할 때까지 유지된다.

### flush와 write-back

```python
def _write_page(self, page: Page) -> None:
    file_path, page_number = parse_page_id(page.page_id)
    handle = self._get_handle(file_path)
    handle.seek(page_number * self.page_size)
    handle.write(page.data)
    handle.flush()
```

디스크 쓰기는 `seek` + `write` + `flush`의 세 단계로 이루어진다. `handle.flush()`가 커널 버퍼까지 밀어넣는다.

## 파일 핸들 관리

```python
def _get_handle(self, file_path: str):
    handle = self.file_handles.get(file_path)
    if handle is None:
        handle = Path(file_path).open("r+b")
        self.file_handles[file_path] = handle
    return handle
```

파일 핸들을 dict로 캐싱한다. 같은 파일에 대해 반복적으로 `open()`하지 않는다. `"r+b"` 모드(읽기+쓰기, 바이너리)로 열어서 같은 핸들로 읽기와 쓰기를 모두 처리한다.

`close()` 메서드에서 `flush_all()` 호출 후 모든 핸들을 닫는다.

## Go 버전과의 차이

| 항목 | Go 07-buffer-pool | Python 04-buffer-pool |
|------|-------------------|----------------------|
| LRU 구현 | 직접 만든 DoublyLinkedList + HashMap | OrderedDict |
| 코드량 | ~200줄 (LRU만 100줄+) | ~130줄 |
| 테스트 수 | 4개 | 7개 |
| 파일 핸들 | os.File | Path.open("r+b") |
| Page ID | 동일 (`파일:번호`) | 동일 |

Python이 더 짧은 이유는 간단하다. OrderedDict가 linked list + hash map의 복합 구조를 이미 구현하고 있기 때문이다. Go에서는 이 구조를 직접 만들어야 했고, 그 과정 자체가 학습 목표였다.

## 마무리

Buffer pool은 "디스크와 메모리 사이의 중재자"다. 모든 페이지 접근은 buffer pool을 통하고, buffer pool이 캐시 히트/미스를 관리하며, dirty page의 안전한 flush를 보장한다. pin count는 "누군가 아직 이 페이지를 쓰고 있다"는 신호이고, 이 신호가 있는 한 페이지는 메모리에서 제거되지 않는다.

소스코드에서 드러나지 않는 핵심: **OrderedDict의 `move_to_end`와 `popitem`이 하는 일이 Go에서는 수십 줄의 pointer 조작이었다.** 언어의 표준 라이브러리가 자료구조 선택을 근본적으로 바꾼다.
