# Distance-Vector Routing 개발 타임라인

## Day 1 — 초기화, Bellman-Ford, 2-phase 시뮬레이션

### Session 1

- 목표: topology loader와 `DVNode.__init__()`에서 각 node가 시작 시점에 "알고 있는 것"을 정리한다.
- 진행: `topology.json`은 `{"x": {"y": 2, "z": 7}, "y": {"x": 2, "z": 1}, "z": {"x": 7, "y": 1}}`처럼 링크 정보를 담고 있다. `load_topology()`는 이 정보를 읽어 bidirectional 구조를 만든다. 처음에는 JSON을 그대로 인접 목록으로 쓰면 된다고 생각했다. 하지만 `z -> x`가 JSON에 없으면 z는 x를 이웃으로 모르고 시작하게 된다.
- 발견: `DVNode.__init__()`의 초기 DV에서 자신은 0, 이웃은 link_cost, 나머지는 INF가 된다. 이 3가지 값을 먼저 읽고 나서야 자신이 모르는 목적지를 어떻게 발견하는지라는 의미가 생긴다.

핵심 코드:

```py
def __init__(self, name: str, neighbors: dict[str, float], all_nodes: list[str]) -> None:
    self.name = name
    self.neighbors = neighbors
    self.neighbor_dvs: dict[str, dict[str, float]] = {}
    self.distance_vector: dict[str, float] = {}
    self.next_hop: dict[str, str] = {}

    for node in all_nodes:
        if node == name:
            self.distance_vector[node] = 0
        elif node in neighbors:
            self.distance_vector[node] = neighbors[node]
        else:
            self.distance_vector[node] = INF
```

```bash
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q \
    study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py::TestDVNodeInit
# 3 passed
```

### Session 2

- 목표: `receive_dv()`에서 Bellman-Ford를 구현하고, `best_hop`까지 연결한다.
- 진행: 이웃에게서 DV를 받으면 `cost_via_v = link_cost + dv.get(dest, INF)`를 전체 목적지에 대해 계산한다. 이 값이 현재 `best_cost`보다 작으면 cost와 hop을 동시에 바꾼다.
- 이슈: 처음에는 cost만 업데이트하고 hop은 다른 루프에서 채우려 했다. cost만 업데이트하면 수렴 후에도 `next_hop`이 없어 routing table이 불완전해진다.
- 측정: triangle test에서 `x -> z`가 z의 직접 링크 7 대신 `via y`로 3 (2+1)을 선택하는지 확인한다.

핵심 코드:

```py
def receive_dv(self, neighbor: str, dv: dict[str, float]) -> bool:
    self.neighbor_dvs[neighbor] = dv
    changed = False
    link_cost = self.neighbors[neighbor]

    for dest in dv:
        cost_via_v = link_cost + dv.get(dest, INF)
        best_cost = self.distance_vector.get(dest, INF)

        if cost_via_v < best_cost:
            self.distance_vector[dest] = cost_via_v
            self.next_hop[dest] = neighbor
            changed = True

    return changed
```

```bash
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q \
    study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py::TestTriangleConvergence
# 3 passed
```

### Session 3

- 목표: 2-phase simulation과 convergence 종료를 완성하고, 11개 단위 테스트를 모두 통과한다.
- 진행: `simulate()`는 round마다 각 node의 DV를 먼저 모두 수집(`messages`)한 자리에, recv를 적용한다. 이 순서가 없으면 같은 round에서 한 노드가 DV를 업데이트한 후 다른 노드가 그 값을 즉시 반영하는 비동기 오염이 만들어진다.
- convergence: `receive_dv()`가 리턴하는 `changed` 보드를 OR하여 어떤 노드도 DV를 바꿀 이유가 없으면 종료한다. 따라서 라운드 제한이 아니라 실질적 변화 여부로 멈춘다.

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/routing/problem test
11 passed in 0.02s
```

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/routing/problem run-solution
=== Iteration 1 ===
Node x: {x: 0, y: 2, z: 3}
Node y: {x: 2, y: 0, z: 1}
Node z: {x: 3, y: 1, z: 0}

=== Final Routing Tables ===
  x -> z: cost=3.0, next_hop=y
  y -> x: cost=2.0, next_hop=x
  z -> x: cost=3.0, next_hop=y
```

- 정리:
  - 초기화 3가지(0 / link_cost / INF)는 언제 나와도 Bellman-Ford가 결정론적인 신호를 주는 근거다.
  - `best_cost`와 `best_hop`을 함께 갱신하지 않으면 routing table이 불완전해진다.
    - 2-phase simulation은 동기적(synchronous) 분산 시스템을 순차 코드로 시뮬레이션하는 가장 단순한 방법이다.
