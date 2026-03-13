# 30 02 WAL Recovery를 다시 검증하고 경계를 닫기

이 글은 프로젝트의 마지막 구간이다. 테스트와 demo를 모두 남겨, 통과 신호와 구현 한계를 한 화면에 붙여 둔다.

## Phase 3
### Session 1

- 당시 목표:
  테스트 명령을 다시 돌려 핵심 invariant가 실제 회귀 신호로 남아 있는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/02-wal-recovery/tests/test_wal_recovery.py`
- 처음 가설:
  pass 수치만 확인하면 충분할 거라고 생각했다.
- 실제 진행:
  `PYTHONPATH=src .venv/bin/python -m pytest`를 다시 실행하고, 어떤 테스트가 있는지 이미 알고 있는 상태에서 pass 신호를 다시 읽었다.

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m pytest
============================= test session starts ==============================
platform darwin -- Python 3.12.6, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/02-wal-recovery
configfile: pyproject.toml
collected 7 items

tests/test_wal_recovery.py .......                                       [100%]

============================== 7 passed in 0.05s ===============================
```

검증 신호:

- `7 passed`
- `test_force_flush_rotates_wal`가 실제로 회귀 테스트 묶음 안에 남아 있다는 점이 중요했다.

핵심 코드:

```python
def test_force_flush_rotates_wal(tmp_path):
    store = DurableStore(tmp_path, 4096, False)
    store.open()
    store.put("alpha", "1")
    store.force_flush()
    wal_path = Path(tmp_path) / "active.wal"
    assert wal_path.stat().st_size == 0
    reopened = DurableStore(tmp_path, 4096, False)
    reopened.open()
    value, found = reopened.get("alpha")
    assert found is True
    assert value == "1"
```

왜 이 코드가 중요했는가:

`test_force_flush_rotates_wal`는 구현의 뒷부분에서 생길 수 있는 붕괴 지점을 문장보다 정확하게 고정한다. pass 숫자보다 중요한 건, 어떤 경계가 계속 회귀 대상으로 남아 있느냐였다.

새로 배운 것:

- 테스트는 단순 성공 여부보다, 어떤 invariant를 공개적으로 약속하는지 보여 주는 문서에 가깝다.

다음:

- demo entry point를 다시 실행해 테스트보다 얇은 표면에서 무엇을 보여 주는지 확인한다.

### Session 2

- 당시 목표:
  demo 출력과 README의 한계를 함께 읽어, 공개 표면과 내부 경계를 분리한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/02-wal-recovery/src/wal_recovery/__main__.py`
- 처음 가설:
  demo는 테스트의 축약판일 뿐이라고 생각했다.
- 실제 진행:
  `PYTHONPATH=src .venv/bin/python -m wal_recovery`를 다시 실행해 마지막 한 줄을 확인하고, README의 `한계와 확장` bullet과 나란히 읽었다.

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m wal_recovery
{'recovered': True, 'value': '1'}
```

검증 신호:

- demo 핵심 줄: `{'recovered': True, 'value': '1'}`
- 경계 메모: 현재 범위 밖: group commit, fsync batching, 압축 로그 세그먼트는 포함하지 않습니다.
- 경계 메모: 현재 범위 밖: 복수 writer와 distributed recovery는 다루지 않습니다.

핵심 코드:

```python
from .store import demo


if __name__ == "__main__":
    demo()
```

왜 이 코드가 중요했는가:

demo entry point는 내부 구현 전체를 보여 주지 않지만, 독자에게 어떤 표면을 공개할지 결정한다. 테스트가 불변식을 지키는 동안 demo는 그중 무엇을 드러낼지 고르는 자리였다.

새로 배운 것:

- `Recovery Policy`에서 정리한 요점처럼, header가 13바이트보다 짧으면 truncated header로 보고 중단한다.

다음:

- 이 프로젝트 이후에는 다음 트랙/다음 슬롯으로 넘어가더라도, 지금 고정한 invariant를 더 큰 저장 엔진이나 분산 경로 안에서 다시 만날 수 있다.
