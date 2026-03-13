# 04 Buffer Pool — Series Map

이 시리즈는 "캐시는 빠르면 된다"라는 흔한 오해를 깨는 데 집중한다. 실제로는 `pin_count`와 `dirty` 때문에, 언제 내보낼 수 있는지가 hit rate만큼 중요했다.

## 이 프로젝트가 답하는 질문

- LRU는 단독으로 충분하지 않다. pinned page를 만나면 eviction은 어떻게 실패해야 하는가
- dirty page write-back을 `flush_page/close`에 묶는 단순화가 학습 단계에서 어떤 장단점을 만드는가

## 읽는 순서

1. [10-chronology-setup-and-surface.md](10-chronology-setup-and-surface.md)
2. [20-chronology-core-mechanics.md](20-chronology-core-mechanics.md)
3. [30-chronology-integration-and-tradeoffs.md](30-chronology-integration-and-tradeoffs.md)
4. [40-chronology-verification-and-boundaries.md](40-chronology-verification-and-boundaries.md)

## 참조한 실제 파일

- `python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`
- `python/database-internals/projects/04-buffer-pool/src/buffer_pool/__main__.py`
- `python/database-internals/projects/04-buffer-pool/tests/test_buffer_pool.py`
- `python/database-internals/projects/04-buffer-pool/README.md`
- `python/database-internals/projects/04-buffer-pool/problem/README.md`
- `python/database-internals/projects/04-buffer-pool/docs/concepts/lru-eviction.md`
- `python/database-internals/projects/04-buffer-pool/docs/concepts/pin-and-dirty.md`
- `python/database-internals/projects/04-buffer-pool/pyproject.toml`

## 재검증 명령

```bash
cd python/database-internals/projects/04-buffer-pool
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m buffer_pool
```

## Git Anchor

- `2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료`
- `2026-03-11 74d5b11 feat: add new project in database-systems`
