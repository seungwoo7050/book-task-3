# 20 핵심 invariant 붙잡기: LRU order, pin count, dirty write-back

이 슬롯의 구현은 크게 두 층으로 나뉜다. `LRUCache`는 순수한 replacement policy를 담당하고, `BufferPool`은 그 위에 page metadata인 `pin_count`와 `dirty`를 얹는다. 실제로 중요한 건 cache가 아니라, 이 두 층이 맞물릴 때 어떤 규칙이 생기는가다.

## Phase 2-1. `LRUCache`는 MRU-first ordering을 고정한다

`LRUCache`는 `OrderedDict`를 사용하고, hit나 insert 때마다 key를 `last=False`로 앞으로 옮긴다. 그래서 `keys()`를 보면 항상 앞쪽이 MRU, 뒤쪽이 LRU다. 테스트 `test_lru_ordering_and_delete`가 바로 이 ordering contract를 잠근다.

이 구조 자체는 익숙하지만, buffer pool 쪽에서 중요해지는 건 이 순서가 eviction candidate를 고르는 출발점이라는 점이다. page metadata는 나중에 붙는다.

## Phase 2-2. `fetch_page()`는 cache hit를 pin 증가와 묶는다

`BufferPool.fetch_page()`를 다시 보면 cache hit는 단순 `return cached`가 아니다. cached page가 있으면 `page.pin_count += 1`을 먼저 하고 돌려준다. 즉 residency는 "캐시에 있느냐"보다 "누가 지금 사용 중이냐"까지 함께 추적된다.

miss일 때도 흐름은 명확하다.

1. `parse_page_id()`로 file path와 page number를 나눈다
2. disk에서 `page_size`만큼 읽어 `Page`를 만든다
3. `pin_count=1`로 cache에 넣는다
4. evicted page가 있으면 pin/dirty 조건을 확인한다

즉 fetch는 lookup과 동시에 pin acquisition이기도 하다.

## Phase 2-3. `unpin_page()`와 `flush_page()`가 dirty write-back 책임을 나눈다

`unpin_page(page_id, is_dirty)`는 이름 그대로 caller가 page 사용을 끝냈다는 신호다. pin_count를 하나 줄이고, `is_dirty=True`면 page를 dirty로 표시한다. 실제 disk write는 여기서 하지 않는다.

write-back은 `flush_page()`와 `flush_all()`이 맡는다. `flush_page()`는 dirty가 아닌 page는 건드리지 않고, dirty page만 `_write_page()`를 거쳐 disk에 쓴 뒤 dirty flag를 내린다. 즉 caller의 수정 사실과 disk 반영 시점이 분리돼 있다.

이 구조는 교육용으로 꽤 좋다. dirty tracking과 write-back policy를 분리해서 보여 주기 때문이다.

## Phase 2-4. source-based seam: pinned eviction 실패는 cache state를 완전히 롤백하지 못한다

이번 Todo에서 가장 중요한 추가 확인은 여기였다. `fetch_page()`는 miss page를 먼저 cache에 `put()`하고, 그 과정에서 evicted page가 나오면 나중에 pin/dirty를 검사한다. 문제는 evicted page가 pinned일 때다. 코드는 evicted page를 다시 `put()`하고 `RuntimeError("bufferpool: cannot evict pinned page")`를 던진다.

보조 재실행을 해 보니 이 경로는 완전한 rollback이 아니었다.

```text
keys_before ['...:1', '...:0'] pin0 1 pin1 0
error RuntimeError bufferpool: cannot evict pinned page
cache_keys_after_error ['...:0', '...:2']
```

즉 pinned page `:0`은 돌아왔지만, 기존 unpinned page `:1`은 사라지고 새 page `:2`가 cache에 남았다. 실패했는데도 cache state가 부분적으로 바뀐 셈이다. 테스트는 현재 이 경로를 직접 다루지 않아서, 문서에는 source+runtime 확인으로 남겨 둘 가치가 있다.

이 seam을 빼고 읽으면 buffer pool이 pin 규칙을 완전히 안전하게 지킨다고 과장하게 된다.
