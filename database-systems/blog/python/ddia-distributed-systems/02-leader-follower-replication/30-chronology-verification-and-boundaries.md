# 30 02 Leader-Follower Replication를 다시 돌려 보며 검증 신호와 경계를 정리하기

이 시리즈의 마지막 글이다. 구현 설명을 닫고, 테스트와 demo가 약속하는 범위를 다시 확인한다. 이때 남는 한계도 함께 적어 둔다.

## Phase 3 — 검증 신호와 한계를 확인하는 구간

이번 글에서는 먼저 테스트가 남긴 회귀 신호를 다시 읽고, 이어서 demo가 공개하는 표면과 README가 남겨 둔 한계를 함께 정리한다.

### Session 1 — 테스트가 남긴 회귀 신호 다시 보기

이번 세션의 목표는 테스트 명령을 다시 돌려 핵심 invariant가 실제 회귀 신호로 남아 있는지 확인하는 것이었다. 초기 가설은 pass 수치만 확인하면 충분할 거라고 생각했다.

막상 다시 펼쳐 보니 `PYTHONPATH=src .venv/bin/python -m pytest`를 다시 실행하고, 어떤 테스트가 있는지 이미 알고 있는 상태에서 pass 신호를 다시 읽었다. 특히 `3 passed`가 이번 판단을 굳혀 줬다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/tests/test_replication.py`

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m pytest
============================= test session starts ==============================
platform darwin -- Python 3.12.6, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication
configfile: pyproject.toml
collected 3 items

tests/test_replication.py ...                                            [100%]

============================== 3 passed in 0.01s ===============================
```

검증 신호:
- `3 passed`
- `test_replicate_once_incremental_and_deletes`가 실제로 회귀 테스트 묶음 안에 남아 있다는 점이 중요했다.

핵심 코드:

```python
def test_replicate_once_incremental_and_deletes():
    leader = Leader()
    follower = Follower()

    leader.put("a", "1")
    assert replicate_once(leader, follower) == 1
    assert follower.watermark() == 0

    leader.put("b", "2")
    leader.delete("a")
    assert replicate_once(leader, follower) == 2
    _value, ok = follower.get("a")
    assert ok is False
    value, ok = follower.get("b")
```

왜 여기서 판단이 바뀌었는가:

`test_replicate_once_incremental_and_deletes`는 구현의 뒷부분에서 생길 수 있는 붕괴 지점을 문장보다 정확하게 고정한다. pass 숫자보다 더 중요했던 건, 어떤 경계가 계속 회귀 테스트로 남아 있느냐였다.

이번 구간에서 새로 이해한 것:
- 테스트는 단순 성공 여부보다, 어떤 invariant를 공개적으로 약속하는지 보여 주는 문서에 가깝다.

다음으로 넘긴 질문:
- demo entry point를 다시 실행해 테스트보다 얇은 표면에서 무엇을 보여 주는지 확인한다.

### Session 2 — demo가 공개하는 표면과 한계 정리하기

이 구간에서 먼저 붙잡으려 한 것은 demo 출력과 README의 한계를 함께 읽어, 공개 표면과 내부 경계를 분리하는 것이었다. 처음 읽을 때는 demo는 테스트의 축약판일 뿐이라고 생각했다.

그런데 `PYTHONPATH=src .venv/bin/python -m leader_follower`를 다시 실행해 마지막 한 줄을 확인하고, README의 `한계와 확장` bullet과 나란히 읽었다. 특히 demo 핵심 줄: `{'applied': 1, 'value': '1'}`라는 출력이 마지막 확인 지점이 됐다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/__main__.py`

CLI:

```bash
$ PYTHONPATH=src .venv/bin/python -m leader_follower
{'applied': 1, 'value': '1'}
```

검증 신호:
- demo 핵심 줄: `{'applied': 1, 'value': '1'}`
- 경계 메모: 현재 범위 밖: automatic leader election과 consensus는 포함하지 않습니다.
- 경계 메모: 현재 범위 밖: quorum write나 multi-leader replication은 다루지 않습니다.

핵심 코드:

```python
from .core import demo


if __name__ == "__main__":
    demo()
```

왜 여기서 판단이 바뀌었는가:

demo entry point는 내부 구현을 전부 보여 주지는 않지만, 독자가 처음 마주치는 공개 표면을 결정한다. 테스트가 invariant를 지키는 장치라면, demo는 그중 무엇을 밖으로 보여 줄지 고르는 자리였다.

이번 구간에서 새로 이해한 것:
- `Idempotent Follower`에서 정리한 요점처럼, 실제 복제에서는 같은 entry batch가 재전송될 수 있다. follower가 `offset <= current_watermark`인 entry를 다시 적용하지 않도록 만들면 replay가 안전해진다.

다음으로 넘긴 질문:
- 이 프로젝트 이후에는 다음 트랙/다음 슬롯으로 넘어가더라도, 지금 고정한 invariant를 더 큰 저장 엔진이나 분산 경로 안에서 다시 만날 수 있다.
