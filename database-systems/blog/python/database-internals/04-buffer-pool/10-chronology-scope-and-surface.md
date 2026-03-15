# 10 범위를 다시 좁히기: 이 슬롯의 중심은 cache가 아니라 page lifecycle이다

처음엔 buffer pool이라면 자연스럽게 hit ratio나 LRU 구현 자체가 중심일 거라고 생각하기 쉽다. 그런데 문제 정의와 테스트를 다시 읽어 보면, 이 슬롯의 진짜 주제는 그보다 좁고 운영적이다. page가 메모리에 올라와 있는 동안 pin 상태가 어떻게 바뀌고, dirty가 언제 디스크에 반영되며, eviction이 어느 조건에서 금지되는지가 핵심이다.

## Phase 1. 테스트가 이미 LRU와 BufferPool을 다른 층으로 나눠 놓는다

`tests/test_buffer_pool.py`는 앞쪽 세 테스트로 `LRUCache`의 기본 순서를 확인하고, 뒤쪽 네 테스트로 `BufferPool`의 page lifecycle을 다룬다.

- `test_lru_basic_operations`
- `test_lru_eviction_and_promotion`
- `test_lru_ordering_and_delete`
- `test_fetch_page_from_disk`
- `test_return_cached_page`
- `test_track_dirty_pages`
- `test_eviction_after_unpin`

이 배치는 꽤 중요하다. 여기서 이미 "replacement policy"와 "page residency semantics"가 같은 문제가 아니라는 사실이 드러난다. LRU는 교체 후보를 정하는 도구고, BufferPool은 그 후보가 실제로 내보낼 수 있는 page인지 pin/dirty 규칙으로 다시 판단한다.

이번 재실행:

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/04-buffer-pool
PYTHONPATH=src python3 -m pytest
```

결과:

```text
7 passed, 1 warning in 0.04s
```

## Phase 2. 문제 정의가 일부러 page allocation보다 "이미 존재하는 file-backed page"에 집중한다

`problem/README.md`를 다시 보면 이 슬롯이 의도적으로 다루지 않는 것도 선명하다. page id는 file path와 page number를 분리해야 하지만, 새 페이지를 allocate하거나 file을 생성하는 경로는 없다. 실제 구현 `_get_handle()`도 `Path(file_path).open("r+b")`를 쓰기 때문에 파일이 이미 존재해야 한다.

즉 이 프로젝트는 완전한 pager가 아니라, "이미 있는 page를 캐시하고 쫓아내는 최소 buffer pool"에 초점을 맞춘다. 그래서 이후 B-tree나 query executor와 연결되기 전의 공통 언어를 만드는 슬롯으로 읽는 편이 자연스럽다.
