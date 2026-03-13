# 20 Core Mechanics

## Day 1
### Session 3

eviction 경로를 읽을 때 가장 중요한 블록은 여기였다.

```python
evicted = self.cache.put(page_id, page)
if evicted is not None:
    evicted_page = evicted.value
    if evicted_page.pin_count > 0:
        self.cache.put(evicted.key, evicted_page)
        raise RuntimeError("bufferpool: cannot evict pinned page")
    if evicted_page.dirty:
        self._write_page(evicted_page)
```

핵심 invariant가 두 개다.

1. `pin_count > 0` 페이지는 절대 내보내지 않는다
2. `dirty` 페이지는 내보내기 전에 디스크로 flush한다

처음엔 pinned 페이지를 만나면 다른 victim을 찾는 loop가 있을 줄 알았는데, 이 프로젝트는 예외를 던져 caller에게 상태를 드러내는 쪽을 택했다. 학습용으로는 이게 더 명확하다.

- 목표: eviction 직전 safety check를 테스트와 함께 검증
- 진행: `test_track_dirty_pages`, `test_eviction_after_unpin`를 코드와 대조

CLI:

```bash
cd python/database-internals/projects/04-buffer-pool
sed -n '52,145p' src/buffer_pool/core.py
sed -n '56,90p' tests/test_buffer_pool.py
```

### Session 4

`unpin_page(page_id, is_dirty)` 설계도 중요한 포인트였다.

```python
if page.pin_count > 0:
    page.pin_count -= 1
if is_dirty:
    page.dirty = True
```

dirty 마킹은 unpin 시점에 caller가 명시적으로 전달한다. 즉 write path가 "데이터 변경"과 "프레임 반환"을 분리해서 표현한다.

다음 질문:

- victim 재시도 정책(clock/2Q)을 붙이면 현재 API는 유지 가능한가
- prefetch/read-ahead를 붙일 때 page_id 모델은 충분한가