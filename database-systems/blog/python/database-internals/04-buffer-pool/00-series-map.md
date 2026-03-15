# 04 Buffer Pool 시리즈 맵

이 프로젝트는 "disk-backed page를 메모리에 캐시한다"는 한 문장보다, `LRU order`, `pin count`, `dirty write-back` 세 규칙이 서로 충돌할 때 어떤 선택을 하는지가 더 중요하다. 읽을 때도 cache API보다 `fetch -> pin/unpin -> eviction/flush` 순서를 먼저 붙드는 편이 맞다.

## 먼저 보고 갈 질문

- cache hit가 단순 반환이 아니라 왜 pin count 증가를 동반해야 하는가?
- dirty page는 언제 write-back되고, pinned page는 어떤 순간에도 eviction되면 안 되는가?
- eviction 실패가 실제로 cache state를 얼마나 안전하게 되돌리는가?

## 읽는 순서

1. [10-chronology-scope-and-surface.md](10-chronology-scope-and-surface.md)
   테스트와 문제 정의를 다시 보며 이 슬롯의 중심이 cache hit ratio보다 page lifecycle 관리라는 점을 먼저 잡는다.
2. [20-chronology-core-invariants.md](20-chronology-core-invariants.md)
   `LRUCache`, `BufferPool.fetch_page()`, `unpin_page()`, `flush_page()`가 실제로 어떤 상태 전이를 고정하는지 본다.
3. [30-chronology-verification-and-boundaries.md](30-chronology-verification-and-boundaries.md)
   pytest, demo, 보조 재실행으로 pin/dirty/eviction 경계와 현재 seam을 정리한다.

## 재검증 명령

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/04-buffer-pool
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m buffer_pool
```

## 이번 시리즈의 근거

- `database-systems/python/database-internals/projects/04-buffer-pool/README.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/problem/README.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/docs/README.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/docs/concepts/lru-eviction.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/docs/concepts/pin-and-dirty.md`
- `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`
- `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/__main__.py`
- `database-systems/python/database-internals/projects/04-buffer-pool/tests/test_buffer_pool.py`

## 보조 메모

작업 메모는 [_evidence-ledger.md](_evidence-ledger.md)와 [_structure-outline.md](_structure-outline.md)에 남긴다. 공개 시리즈는 `00 -> 10 -> 20 -> 30`만 읽어도 충분하다.
