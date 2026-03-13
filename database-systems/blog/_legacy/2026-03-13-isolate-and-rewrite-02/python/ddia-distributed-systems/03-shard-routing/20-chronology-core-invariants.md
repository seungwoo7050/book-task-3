# 20 03 Shard Routing의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `Router`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py`의 `Router`
- 처음 가설:
  `Router` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "Router|hash_value" src`로 핵심 함수 위치를 다시 잡고, `Router`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "Router|hash_value" src
src/shard_routing/core.py:8:def hash_value(value: str) -> int:
src/shard_routing/core.py:14:    hash_value: int
src/shard_routing/core.py:29:            entry = RingEntry(hash_value(f"{node_id}#v{index}"), node_id)
src/shard_routing/core.py:42:        target = hash_value(key)
src/shard_routing/core.py:43:        hashes = [entry.hash_value for entry in self.ring]
src/shard_routing/core.py:62:class Router:
src/shard_routing/core.py:82:    router = Router(ring)
src/shard_routing/__init__.py:1:from .core import Ring, Router
src/shard_routing/__init__.py:3:__all__ = ["Ring", "Router"]
```

검증 신호:

- `Router` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `consistent hash ring이 key를 물리 node에 매핑하는 방식을 익힙니다.`

핵심 코드:

```python
class Router:
    def __init__(self, ring: Ring) -> None:
        self.ring = ring

    def route(self, key: str) -> tuple[str, bool]:
        return self.ring.node_for_key(key)

    def route_batch(self, keys: list[str]) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = {}
        for key in keys:
            node_id, ok = self.ring.node_for_key(key)
            if ok:
                grouped.setdefault(node_id, []).append(key)
        return grouped
```

왜 이 코드가 중요했는가:

`Router`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Virtual Nodes`에서 정리한 요점처럼, 물리 node마다 ring에 하나의 점만 두면 hash 편차 때문에 분산이 쉽게 치우친다. virtual node는 물리 node 하나를 ring 위의 여러 점으로 쪼개서 더 고르게 분산되도록 만든다.

다음:

- `hash_value`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `hash_value`가 `Router`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/python/ddia-distributed-systems/projects/03-shard-routing/src/shard_routing/core.py`의 `hash_value`
- 처음 가설:
  `hash_value`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `Router`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(class|def) " src
src/shard_routing/core.py:8:def hash_value(value: str) -> int:
src/shard_routing/core.py:13:class RingEntry:
src/shard_routing/core.py:18:class Ring:
src/shard_routing/core.py:62:class Router:
src/shard_routing/core.py:78:def demo() -> None:
```

검증 신호:

- `hash_value`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_batch_routing` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
def hash_value(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")


@dataclass(slots=True, order=True)
class RingEntry:
    hash_value: int
    node_id: str
```

왜 이 코드가 중요했는가:

`hash_value`가 없으면 `Router`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Virtual Nodes`에서 정리한 요점처럼, 물리 node마다 ring에 하나의 점만 두면 hash 편차 때문에 분산이 쉽게 치우친다. virtual node는 물리 node 하나를 ring 위의 여러 점으로 쪼개서 더 고르게 분산되도록 만든다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
