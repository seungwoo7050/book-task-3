# 30 다시 돌려 보기: buffer pool이 현재 실제로 보장하는 것

마지막으로 남는 건 숫자와 경계다. buffer pool은 작은 코드로도 "거의 다 된 것처럼" 보이기 쉬운데, 테스트가 덮는 범위와 보조 재실행에서만 드러나는 seam을 같이 봐야 실제 현재 상태가 보인다.

## Phase 3-1. pytest는 기본 lifecycle은 잘 잠그지만, 실패 rollback까진 보지 않는다

이번 재실행에서 pytest는 `7 passed, 1 warning in 0.04s`였다. 경고는 앞 슬롯들과 같은 `pytest_asyncio` deprecation이라 핵심과는 무관했다.

테스트가 실제로 잠그는 건 이 정도다.

- LRU basic ordering
- LRU promotion/eviction
- page fetch from disk
- cached page 재사용
- dirty flag tracking
- unpin 후 eviction 가능

즉 happy path와 정상 lifecycle은 꽤 잘 덮는다. 하지만 pinned eviction failure와 dirty page eviction write-back 결과가 disk bytes에 어떻게 남는지는 현재 테스트가 직접 보지 않는다.

## Phase 3-2. demo는 가장 얇은 public surface만 보여 준다

demo entry point는 page 하나를 fetch해 prefix를 보여 준다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/04-buffer-pool
PYTHONPATH=src python3 -m buffer_pool
```

출력:

```text
{'page_id': '.../data.db:0', 'pin_count': 1, 'prefix': 'page-0'}
```

이 한 줄은 fetch 후 pin_count가 1이라는 가장 기본 표면만 드러낸다. dirty, flush, eviction은 demo가 아니라 테스트와 source가 설명하는 영역으로 남아 있다.

## Phase 3-3. 보조 재실행이 현재 seam을 더 분명히 보여 줬다

이번 Todo에서 pinned page가 LRU일 때 eviction을 일부러 유도해 봤다. 결과는 중요했다.

- `RuntimeError bufferpool: cannot evict pinned page`
- 하지만 error 뒤 cache keys는 `['...:0', '...:2']`

즉 실패한 fetch가 완전히 원상복구되진 않는다. 새 page가 남고, 기존 unpinned page 하나가 사라질 수 있다. 이건 buffer pool 교체 경계에서 꽤 큰 현재 seam이다.

또 다른 현재 경계도 선명하다.

- `_get_handle()`는 `r+b`만 쓰므로 file은 미리 존재해야 한다
- `close()`는 `flush_all()` 뒤 file handles를 닫는다
- dirty page write-back은 synchronous `handle.write()` + `flush()`다

즉 이 프로젝트는 최소 buffer pool manager이지, page allocator나 async pager는 아니다.

## Phase 3-4. 지금 상태에서 비워 둔 것

- concurrent latch가 없다
- page allocation/deallocation이 없다
- dirty eviction의 disk outcome을 직접 검증하는 테스트가 없다
- failed eviction rollback이 완전하지 않다
- clock replacer, background flush worker, metrics가 없다

그래도 이 프로젝트가 중요한 이유는 분명하다. 앞선 슬롯들이 bytes와 records를 다뤘다면, 여기선 처음으로 page residency와 cache replacement를 구체적인 metadata로 다루기 시작한다. 이후 B-tree나 더 높은 read path를 올릴 때 필요한 vocabulary가 바로 여기서 생긴다.
