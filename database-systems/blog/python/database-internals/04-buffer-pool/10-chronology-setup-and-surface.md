# 10 cache 가 아니라 page lifecycle 을 다루는 단계

## Day 1
### Session 1

처음에는 LRU 예제라고 가볍게 봤다. 그런데 `Page` 구조를 보면 의도가 다르다.

```python
@dataclass(slots=True)
class Page:
    page_id: str
    data: bytearray
    dirty: bool = False
    pin_count: int = 0
```

`dirty`와 `pin_count`가 함께 있는 순간 이건 단순 캐시가 아니다. "지금 내보내도 되는 페이지인가"를 판단하는 buffer manager다.

- 목표: 이 프로젝트가 LRU 구현 연습인지, buffer lifecycle 학습인지 구분
- 진행: `LRUCache`보다 `BufferPool.fetch_page/unpin_page/flush_page`를 먼저 읽음

CLI:

```bash
cd python/database-internals/projects/04-buffer-pool
grep -n "def test_" tests/test_buffer_pool.py
```

```text
40:def test_fetch_page_from_disk(tmp_path):
48:def test_return_cached_page(tmp_path):
56:def test_track_dirty_pages(tmp_path):
65:def test_eviction_after_unpin(tmp_path):
```

테스트도 page 상태 전이에 맞춰져 있다.

### Session 2

`fetch_page()`의 hit 경로를 보면 pin count를 바로 올린다.

```python
cached = self.cache.get(page_id)
if cached is not None:
    page = cached
    page.pin_count += 1
    return page
```

즉 buffer pool이 반환하는 객체는 read-only snapshot이 아니라 "사용 중인 프레임"이다. caller가 `unpin_page()`를 호출해줘야 eviction 후보가 된다.

다음 질문:

- eviction 직전 pinned/dirty 페이지는 어떻게 처리되는가
- close 시점 flush 정책은 어디서 고정되는가