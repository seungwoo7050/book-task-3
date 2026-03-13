# 30 04 Buffer Pool를 다시 검증하고 경계를 닫기

이 글은 프로젝트의 마지막 구간이다. 테스트와 demo를 모두 남겨, 통과 신호와 구현 한계를 한 화면에 붙여 둔다.

## Phase 3
### Session 1

- 당시 목표:
  테스트 명령을 다시 돌려 핵심 invariant가 실제 회귀 신호로 남아 있는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/04-buffer-pool/tests/test_buffer_pool.py`
- 처음 가설:
  pass 수치만 확인하면 충분할 거라고 생각했다.
- 실제 진행:
  `PYTHONPATH=src .venv/bin/python -m pytest`를 다시 실행하고, 어떤 테스트가 있는지 이미 알고 있는 상태에서 pass 신호를 다시 읽었다.

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m pytest
============================= test session starts ==============================
platform darwin -- Python 3.12.6, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/04-buffer-pool
configfile: pyproject.toml
collected 7 items

tests/test_buffer_pool.py .......                                        [100%]

============================== 7 passed in 0.06s ===============================
```

검증 신호:

- `7 passed`
- `test_lru_ordering_and_delete`가 실제로 회귀 테스트 묶음 안에 남아 있다는 점이 중요했다.

핵심 코드:

```python
def test_lru_ordering_and_delete():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.keys() == ["c", "b", "a"]
    cache.get("a")
    assert cache.keys() == ["a", "c", "b"]
    assert cache.delete("a") is True
    assert cache.delete("missing") is False
```

왜 이 코드가 중요했는가:

`test_lru_ordering_and_delete`는 구현의 뒷부분에서 생길 수 있는 붕괴 지점을 문장보다 정확하게 고정한다. pass 숫자보다 중요한 건, 어떤 경계가 계속 회귀 대상으로 남아 있느냐였다.

새로 배운 것:

- 테스트는 단순 성공 여부보다, 어떤 invariant를 공개적으로 약속하는지 보여 주는 문서에 가깝다.

다음:

- demo entry point를 다시 실행해 테스트보다 얇은 표면에서 무엇을 보여 주는지 확인한다.

### Session 2

- 당시 목표:
  demo 출력과 README의 한계를 함께 읽어, 공개 표면과 내부 경계를 분리한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/04-buffer-pool/src/buffer_pool/__main__.py`
- 처음 가설:
  demo는 테스트의 축약판일 뿐이라고 생각했다.
- 실제 진행:
  `PYTHONPATH=src .venv/bin/python -m buffer_pool`를 다시 실행해 마지막 한 줄을 확인하고, README의 `한계와 확장` bullet과 나란히 읽었다.

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m buffer_pool
{'page_id': '/var/folders/92/jftxv3md5_z3jr5ybm1c3yx40000gn/T/buffer-pool-gg0isyxk/data.db:0', 'pin_count': 1, 'prefix': 'page-0'}
```

검증 신호:

- demo 핵심 줄: `{'page_id': '/var/folders/92/jftxv3md5_z3jr5ybm1c3yx40000gn/T/buffer-pool-gg0isyxk/data.db`
- 경계 메모: 현재 범위 밖: concurrent latch, lock manager, asynchronous IO는 포함하지 않습니다.
- 경계 메모: 현재 범위 밖: buffer pool을 B-tree나 query executor와 연결하는 단계는 후속 범위로 남깁니다.

핵심 코드:

```python
from .core import demo


if __name__ == "__main__":
    demo()
```

왜 이 코드가 중요했는가:

demo entry point는 내부 구현 전체를 보여 주지 않지만, 독자에게 어떤 표면을 공개할지 결정한다. 테스트가 불변식을 지키는 동안 demo는 그중 무엇을 드러낼지 고르는 자리였다.

새로 배운 것:

- `LRU Eviction`에서 정리한 요점처럼, doubly-linked list와 hash map을 조합하면 O(1) get/put/evict가 가능하다.

다음:

- 이 프로젝트 이후에는 다음 트랙/다음 슬롯으로 넘어가더라도, 지금 고정한 invariant를 더 큰 저장 엔진이나 분산 경로 안에서 다시 만날 수 있다.
