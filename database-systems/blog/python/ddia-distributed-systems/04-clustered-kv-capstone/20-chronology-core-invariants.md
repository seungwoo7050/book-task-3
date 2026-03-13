# 20 04 Clustered KV Capstone에서 진짜 중요한 상태 전이만 붙잡기

이 시리즈의 가운데 글이다. 기능 목록을 다시 적기보다, 규칙이 실제 코드에서 언제 강제되는지 보여 주는 데 초점을 둔다.

## Phase 2 — 핵심 상태 전이를 붙잡는 구간

이번 글에서는 핵심 함수 두 곳을 따라가며 같은 invariant가 어디서 고정되고, 다른 각도에서 어떻게 반복되는지 본다.

### Session 1 — ShardRing에서 invariant가 잠기는 지점 보기

이번 세션의 목표는 `ShardRing`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해하는 것이었다. 초기 가설은 `ShardRing` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.

막상 다시 펼쳐 보니 `rg -n "ShardRing|DiskStore" src`로 핵심 함수 위치를 다시 잡고, `ShardRing`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다. 특히 `ShardRing` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py`의 `ShardRing`

CLI:

```bash
$ rg -n "ShardRing|DiskStore" src
src/clustered_kv/core.py:22:class DiskStore:
src/clustered_kv/core.py:91:    stores: dict[str, DiskStore] = field(default_factory=dict)
src/clustered_kv/core.py:100:class ShardRing:
src/clustered_kv/core.py:121:        self.router = ShardRing(virtual_nodes)
src/clustered_kv/core.py:129:                node.stores[group.shard_id] = DiskStore(self.data_dir / node_id / f"{group.shard_id}.log")
```

검증 신호:
- `ShardRing` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `router, leader, follower, local store가 한 write pipeline 안에서 어떻게 연결되는지 익힙니다.`

핵심 코드:

```python
class ShardRing:
    def __init__(self, virtual_nodes: int = 64) -> None:
        self.virtual_nodes = virtual_nodes or 64
        self.ring: list[RingEntry] = []

    def add_shard(self, shard_id: str) -> None:
        for index in range(self.virtual_nodes):
            bisect.insort(self.ring, RingEntry(hash_value(f"{shard_id}#v{index}"), shard_id))

    def shard_for_key(self, key: str) -> str:
        target = hash_value(key)
        hashes = [entry.hash_value for entry in self.ring]
        index = bisect.bisect_left(hashes, target)
        if index == len(self.ring):
```

왜 여기서 판단이 바뀌었는가:

`ShardRing`는 이 프로젝트에서 규칙이 가장 먼저 굳는 지점을 보여 준다. 테스트가 요구한 첫 번째 조건이 실제 코드 규칙으로 바뀌는 순간을 여기서 확인할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Static Topology`에서 정리한 요점처럼, 이 capstone은 membership change 자체를 다루지 않는다. shard 집합과 각 shard의 leader/follower 배치는 초기화 시점에 고정된다.

다음으로 넘긴 질문:
- `DiskStore`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2 — DiskStore로 같은 규칙 다시 확인하기

이 구간에서 먼저 붙잡으려 한 것은 `DiskStore`가 `ShardRing`와 어떤 짝을 이루는지 확인하는 것이었다. 처음 읽을 때는 `DiskStore`는 단순 보조 함수일 거라고 생각했다.

그런데 두 번째 앵커를 읽고 나니, 실제로는 `ShardRing`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다. 특히 `DiskStore`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py`의 `DiskStore`

CLI:

```bash
$ rg -n "^(class|def) " src
src/clustered_kv/app.py:12:class ValuePayload(BaseModel):
src/clustered_kv/app.py:16:def create_app(cluster: Cluster) -> FastAPI:
src/clustered_kv/app.py:37:def demo() -> None:
src/clustered_kv/core.py:10:def hash_value(value: str) -> int:
src/clustered_kv/core.py:15:class Operation:
src/clustered_kv/core.py:22:class DiskStore:
src/clustered_kv/core.py:82:class ReplicaGroup:
src/clustered_kv/core.py:89:class Node:
src/clustered_kv/core.py:95:class RingEntry:
src/clustered_kv/core.py:100:class ShardRing:
src/clustered_kv/core.py:118:class Cluster:
```

검증 신호:
- `DiskStore`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_restart_node_loads_from_disk` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
class DiskStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data: dict[str, str] = {}
        self.log: list[Operation] = []
        self._load()

    def _load(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        self.data = {}
        self.log = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line:
```

왜 여기서 판단이 바뀌었는가:

`DiskStore`가 없으면 `ShardRing`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

이번 구간에서 새로 이해한 것:
- `Static Topology`에서 정리한 요점처럼, 이 capstone은 membership change 자체를 다루지 않는다. shard 집합과 각 shard의 leader/follower 배치는 초기화 시점에 고정된다.

다음으로 넘긴 질문:
- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
