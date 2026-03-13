# 20 02 Leader-Follower Replication의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `replicate_once`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py`의 `replicate_once`
- 처음 가설:
  `replicate_once` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "replicate_once|Follower" src`로 핵심 함수 위치를 다시 잡고, `replicate_once`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "replicate_once|Follower" src
src/leader_follower/core.py:53:class Follower:
src/leader_follower/core.py:78:def replicate_once(leader: Leader, follower: Follower) -> int:
src/leader_follower/core.py:85:    follower = Follower()
src/leader_follower/core.py:87:    applied = replicate_once(leader, follower)
src/leader_follower/__init__.py:1:from .core import Follower, Leader, ReplicationLog, replicate_once
src/leader_follower/__init__.py:3:__all__ = ["Follower", "Leader", "ReplicationLog", "replicate_once"]
```

검증 신호:

- `replicate_once` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `leader가 local state와 append-only log를 어떻게 함께 유지하는지 익힙니다.`

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

`replicate_once`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Log Shipping`에서 정리한 요점처럼, leader-follower 복제의 핵심은 "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이다. follower는 leader의 현재 key-value map을 통째로 받지 않고, 자신이 마지막으로 적용한 offset 이후의 entry만 가져온다.

다음:

- `Follower`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `Follower`가 `replicate_once`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py`의 `Follower`
- 처음 가설:
  `Follower`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `replicate_once`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

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

- `Follower`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_replicate_once_incremental_and_deletes` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
class Follower:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.last_applied_offset = -1

    def apply(self, entries: list[LogEntry]) -> int:
        applied = 0
        for entry in entries:
            if entry.offset <= self.last_applied_offset:
                continue
            if entry.operation == "put" and entry.value is not None:
                self.store[entry.key] = entry.value
            if entry.operation == "delete":
                self.store.pop(entry.key, None)
```

왜 이 코드가 중요했는가:

`Follower`가 없으면 `replicate_once`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Log Shipping`에서 정리한 요점처럼, leader-follower 복제의 핵심은 "store state 자체"보다 "state를 만든 ordered mutation stream"을 보내는 것이다. follower는 leader의 현재 key-value map을 통째로 받지 않고, 자신이 마지막으로 적용한 offset 이후의 entry만 가져온다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
