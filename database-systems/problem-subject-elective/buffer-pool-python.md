# buffer-pool-python 문제지

## 왜 중요한가

page id로 file path와 page number를 안정적으로 분리해야 합니다. fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다. dirty page는 eviction이나 explicit flush 때 write-back해야 합니다. pinned page는 eviction하면 안 됩니다.

## 목표

시작 위치의 구현을 완성해 page id로 file path와 page number를 안정적으로 분리해야 합니다, fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다, dirty page는 eviction이나 explicit flush 때 write-back해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../python/database-internals/projects/04-buffer-pool/src/buffer_pool/__init__.py`
- `../python/database-internals/projects/04-buffer-pool/src/buffer_pool/__main__.py`
- `../python/database-internals/projects/04-buffer-pool/src/buffer_pool/core.py`
- `../python/database-internals/projects/04-buffer-pool/tests/test_buffer_pool.py`
- `../python/database-internals/projects/04-buffer-pool/pyproject.toml`

## starter code / 입력 계약

- `../python/database-internals/projects/04-buffer-pool/src/buffer_pool/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- page id로 file path와 page number를 안정적으로 분리해야 합니다.
- fetch 시 cache hit면 pin count를 올리고, miss면 disk read 후 캐시에 올려야 합니다.
- dirty page는 eviction이나 explicit flush 때 write-back해야 합니다.
- pinned page는 eviction하면 안 됩니다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `Entry`와 `LRUCache`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_lru_basic_operations`와 `test_lru_eviction_and_promotion`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/04-buffer-pool && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/04-buffer-pool && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`buffer-pool-python_answer.md`](buffer-pool-python_answer.md)에서 확인한다.
