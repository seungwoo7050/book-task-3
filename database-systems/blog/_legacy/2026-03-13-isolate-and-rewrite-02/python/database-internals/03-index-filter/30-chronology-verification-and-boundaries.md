# 30 03 Index Filter를 다시 검증하고 경계를 닫기

이 글은 프로젝트의 마지막 구간이다. 테스트와 demo를 모두 남겨, 통과 신호와 구현 한계를 한 화면에 붙여 둔다.

## Phase 3
### Session 1

- 당시 목표:
  테스트 명령을 다시 돌려 핵심 invariant가 실제 회귀 신호로 남아 있는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/03-index-filter/tests/test_index_filter.py`
- 처음 가설:
  pass 수치만 확인하면 충분할 거라고 생각했다.
- 실제 진행:
  `PYTHONPATH=src .venv/bin/python -m pytest`를 다시 실행하고, 어떤 테스트가 있는지 이미 알고 있는 상태에서 pass 신호를 다시 읽었다.

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m pytest
============================= test session starts ==============================
platform darwin -- Python 3.12.6, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter
configfile: pyproject.toml
collected 4 items

tests/test_index_filter.py ....                                          [100%]

============================== 4 passed in 0.07s ===============================
```

검증 신호:

- `4 passed`
- `test_sstable_bloom_reject_and_bounded_scan`가 실제로 회귀 테스트 묶음 안에 남아 있다는 점이 중요했다.

핵심 코드:

```python
def test_sstable_bloom_reject_and_bounded_scan(tmp_path):
    table = SSTable(tmp_path / "index.sst", 8)
    records = [(fmt_key(index), f"value-{fmt_key(index)}") for index in range(64)]
    table.write(records)

    value, ok, stats, _ = table.get_with_stats("missing-key")
    assert ok is False
    assert value is None
    assert stats.bloom_rejected is True
    assert stats.bytes_read == 0
```

왜 이 코드가 중요했는가:

`test_sstable_bloom_reject_and_bounded_scan`는 구현의 뒷부분에서 생길 수 있는 붕괴 지점을 문장보다 정확하게 고정한다. pass 숫자보다 중요한 건, 어떤 경계가 계속 회귀 대상으로 남아 있느냐였다.

새로 배운 것:

- 테스트는 단순 성공 여부보다, 어떤 invariant를 공개적으로 약속하는지 보여 주는 문서에 가깝다.

다음:

- demo entry point를 다시 실행해 테스트보다 얇은 표면에서 무엇을 보여 주는지 확인한다.

### Session 2

- 당시 목표:
  demo 출력과 README의 한계를 함께 읽어, 공개 표면과 내부 경계를 분리한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/03-index-filter/src/index_filter/__main__.py`
- 처음 가설:
  demo는 테스트의 축약판일 뿐이라고 생각했다.
- 실제 진행:
  `PYTHONPATH=src .venv/bin/python -m index_filter`를 다시 실행해 마지막 한 줄을 확인하고, README의 `한계와 확장` bullet과 나란히 읽었다.

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m index_filter
{'found': True, 'value': 'value-k023', 'bytes_read': 176}
```

검증 신호:

- demo 핵심 줄: `{'found': True, 'value': 'value-k023', 'bytes_read': 176}`
- 경계 메모: 현재 범위 밖: learned index와 adaptive filter는 포함하지 않습니다.
- 경계 메모: 현재 범위 밖: range query 최적화와 block cache 연동은 다음 단계 확장으로 남깁니다.

핵심 코드:

```python
from .table import demo


if __name__ == "__main__":
    demo()
```

왜 이 코드가 중요했는가:

demo entry point는 내부 구현 전체를 보여 주지 않지만, 독자에게 어떤 표면을 공개할지 결정한다. 테스트가 불변식을 지키는 동안 demo는 그중 무엇을 드러낼지 고르는 자리였다.

새로 배운 것:

- `Bloom Filter Sizing`에서 정리한 요점처럼, Bloom filter는 false negative가 없어야 하고, false positive는 허용 가능한 수준으로만 남아야 한다. 이 프로젝트는 레거시와 같은 식을 사용한다.

다음:

- 이 프로젝트 이후에는 다음 트랙/다음 슬롯으로 넘어가더라도, 지금 고정한 invariant를 더 큰 저장 엔진이나 분산 경로 안에서 다시 만날 수 있다.
