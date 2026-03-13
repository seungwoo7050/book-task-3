# 10 04 Clustered KV Capstone를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. 설명문을 믿고 곧장 구현으로 들어가기보다, 테스트와 파일 구조를 다시 읽으면서 어디서부터 이야기를 시작해야 하는지 정리한다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

여기서 가장 먼저 확인한 것은 `04 Clustered KV Capstone`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다. 처음에는 README의 한 줄 설명만으로는 실제 핵심 invariant가 무엇인지 아직 흐릿했다.

하지만 실제로는 `find src tests -type f | sort`로 구조를 펼친 뒤 `rg -n "^def test_" tests`로 테스트 이름을 나열했다. `test_restart_node_loads_from_disk`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `ShardRing` 주변의 invariant를 고정하는 일이라는 게 보였다. 결정적으로 방향을 잡아 준 신호는 `test_write_routes_to_leader_and_replicates`는 가장 기본 표면을 보여 줬고, `test_restart_node_loads_from_disk`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/README.md`, `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/tests/test_clustered_kv.py`

CLI:

```bash
$ find src tests -type f | sort
src/clustered_kv/__init__.py
src/clustered_kv/__main__.py
src/clustered_kv/__pycache__/__init__.cpython-312.pyc
src/clustered_kv/__pycache__/__init__.cpython-314.pyc
src/clustered_kv/__pycache__/__main__.cpython-312.pyc
src/clustered_kv/__pycache__/__main__.cpython-314.pyc
src/clustered_kv/__pycache__/app.cpython-312.pyc
src/clustered_kv/__pycache__/app.cpython-314.pyc
src/clustered_kv/__pycache__/core.cpython-312.pyc
src/clustered_kv/__pycache__/core.cpython-314.pyc
src/clustered_kv/app.py
src/clustered_kv/core.py
src/clustered_kv_capstone.egg-info/PKG-INFO
src/clustered_kv_capstone.egg-info/SOURCES.txt
src/clustered_kv_capstone.egg-info/dependency_links.txt
src/clustered_kv_capstone.egg-info/requires.txt
src/clustered_kv_capstone.egg-info/top_level.txt
tests/__pycache__/test_clustered_kv.cpython-312-pytest-8.3.5.pyc
tests/__pycache__/test_clustered_kv.cpython-314-pytest-8.4.2.pyc
tests/__pycache__/test_clustered_kv.cpython-314-pytest-9.0.2.pyc
tests/test_clustered_kv.py
```

```bash
$ rg -n "^def test_" tests
tests/test_clustered_kv.py:6:def test_write_routes_to_leader_and_replicates(tmp_path):
tests/test_clustered_kv.py:20:def test_follower_catch_up_and_delete(tmp_path):
tests/test_clustered_kv.py:41:def test_restart_node_loads_from_disk(tmp_path):
tests/test_clustered_kv.py:53:def test_fastapi_round_trip(tmp_path):
```

검증 신호:
- `test_write_routes_to_leader_and_replicates`는 가장 기본 표면을 보여 줬고, `test_restart_node_loads_from_disk`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `ShardRing` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```python
def test_restart_node_loads_from_disk(tmp_path):
    cluster = new_cluster(tmp_path)
    shard_id = cluster.put("gamma", "3")
    group = cluster.group(shard_id)
    follower = group.followers[0]

    cluster.restart_node(follower)
    value, ok = cluster.read_from_node(follower, "gamma")
    assert ok is True
    assert value == "3"
```

왜 여기서 판단이 바뀌었는가:

`test_restart_node_loads_from_disk`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Replicated Write Pipeline`에서 정리한 요점처럼, write pipeline은 다음 순서를 따른다.

다음으로 넘긴 질문:
- `ShardRing`와 `DiskStore`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

이번 세션의 목표는 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인하는 것이었다. 초기 가설은 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

막상 다시 펼쳐 보니 가장 큰 구현 파일인 `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 특히 `ShardRing` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone/src/clustered_kv/core.py`

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
- `ShardRing` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `DiskStore`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

`ShardRing`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Static Topology`에서 정리한 요점처럼, 이 capstone은 membership change 자체를 다루지 않는다. shard 집합과 각 shard의 leader/follower 배치는 초기화 시점에 고정된다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `DiskStore`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
