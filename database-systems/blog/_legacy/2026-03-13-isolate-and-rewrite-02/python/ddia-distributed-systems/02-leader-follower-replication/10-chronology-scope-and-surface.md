# 10 02 Leader-Follower Replication의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `02 Leader-Follower Replication`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/README.md`, `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/tests/test_replication.py`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find src tests -type f | sort`로 구조를 펼친 뒤 `rg -n "^def test_" tests`로 테스트 이름을 나열했다. `test_replicate_once_incremental_and_deletes`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `replicate_once` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find src tests -type f | sort
src/leader_follower/__init__.py
src/leader_follower/__main__.py
src/leader_follower/__pycache__/__init__.cpython-312.pyc
src/leader_follower/__pycache__/__init__.cpython-314.pyc
src/leader_follower/__pycache__/__main__.cpython-312.pyc
src/leader_follower/__pycache__/__main__.cpython-314.pyc
src/leader_follower/__pycache__/core.cpython-312.pyc
src/leader_follower/__pycache__/core.cpython-314.pyc
src/leader_follower/core.py
tests/__pycache__/test_replication.cpython-312-pytest-8.3.5.pyc
tests/__pycache__/test_replication.cpython-314-pytest-9.0.2.pyc
tests/test_replication.py
```

```bash
$ rg -n "^def test_" tests
tests/test_replication.py:4:def test_replication_log_assigns_sequential_offsets():
tests/test_replication.py:10:def test_follower_apply_is_idempotent():
tests/test_replication.py:23:def test_replicate_once_incremental_and_deletes():
```

검증 신호:

- `test_replication_log_assigns_sequential_offsets`는 가장 기본 표면을 보여 줬고, `test_replicate_once_incremental_and_deletes`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `replicate_once` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

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

왜 이 코드가 중요했는가:

`test_replicate_once_incremental_and_deletes`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Idempotent Follower`에서 정리한 요점처럼, 실제 복제에서는 같은 entry batch가 재전송될 수 있다. follower가 `offset <= current_watermark`인 entry를 다시 적용하지 않도록 만들면 replay가 안전해진다.

다음:

- `replicate_once`와 `Follower`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

CLI:

```bash
$ rg -n "^(class|def) " src
src/leader_follower/core.py:7:class LogEntry:
src/leader_follower/core.py:14:class ReplicationLog:
src/leader_follower/core.py:30:class Leader:
src/leader_follower/core.py:53:class Follower:
src/leader_follower/core.py:78:def replicate_once(leader: Leader, follower: Follower) -> int:
src/leader_follower/core.py:83:def demo() -> None:
```

검증 신호:

- `replicate_once` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `Follower`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

핵심 코드:

```python
def replicate_once(leader: Leader, follower: Follower) -> int:
    entries = leader.log_from(follower.watermark() + 1)
    return follower.apply(entries)


def demo() -> None:
    leader = Leader()
    follower = Follower()
    leader.put("alpha", "1")
    applied = replicate_once(leader, follower)
    print({"applied": applied, "value": follower.get("alpha")[0]})
```

왜 이 코드가 중요했는가:

`replicate_once`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `Log Shipping`에서 정리한 요점처럼, leader-follower 복제의 핵심은 "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이다. follower는 leader의 현재 key-value map을 통째로 받지 않고, 자신이 마지막으로 적용한 offset 이후의 entry만 가져온다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `Follower`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
