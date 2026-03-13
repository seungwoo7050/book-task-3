# Distance-Vector Routing development timeline

`Distance-Vector Routing`를 읽을 때 먼저 잡아야 하는 것은 기능 목록이 아니라, 어디서부터 구현이나 분석이 무거워졌는가이다.

그래서 이 문서는 문제 문서, 핵심 파일, 테스트, CLI 출력만 남기고 나머지 군더더기는 걷어 냈다.

## 구현 순서 한눈에 보기

1. `study/04-Network-Diagnostics-and-Routing/routing/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 실행 표면과 entrypoint를 먼저 고정하기

이 단계에서는 구현 세부로 바로 내려가지 않았다. 먼저 어떤 파일이 진입점이고 어떤 명령이 검증 기준인지 고정하는 일이 더 급했다.

- 당시 목표: `Distance-Vector Routing`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `def load_topology`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: Bellman-Ford update 식

핵심 코드/trace:

```python
def load_topology(filepath: str) -> tuple[list[str], dict[str, dict[str, int]]]:
    """JSON file에서 network topology를 읽는다.

    Args:
        filepath: topology JSON file path.

    Returns:
        `(node_list, adjacency_dict)` tuple.
        `adjacency_dict`는 `node -> {neighbor: cost}`를 뜻한다.
    """
```

왜 이 코드가 중요했는가:

문제 사양을 읽은 뒤 바로 이 지점으로 내려오면, 말로 적힌 요구가 실제 파일 구조와 어떻게 만나는지 곧바로 보인다.

CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/routing/problem help
  run-sim              Run the skeleton DV simulation
  run-solution         Run the solution DV simulation
  test                 Run the test script
```

## 2. Bellman-Ford 갱신을 node 단위 상태 변화로 읽기

중간 단계의 핵심은 '무엇을 만들었나'보다 '어느 줄에서 규칙이 드러나는가'를 잡는 일이었다.

- 당시 목표: `Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제입니다.`를 실제 근거에 붙인다.
- 실제 진행: `def receive_dv` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: 2-phase synchronous simulation

핵심 코드/trace:

```python
def receive_dv(self, sender: str, dv: dict[str, float]) -> bool:
        """neighbor에게서 받은 distance vector를 반영한다.

        Args:
            sender: The neighbor that sent this DV.
            dv: The neighbor's distance vector.

        Returns:
            True if this node's DV changed, False otherwise.
        """
```

왜 이 코드가 중요했는가:

핵심은 함수 이름 자체가 아니라, 이 줄 주변에서 어떤 입력이 어떤 결과로 바뀌는지가 한 번에 드러난다는 점이다.

CLI:

```bash
$ rg -n -e 'def load_topology' -e 'class DVNode' -e 'def receive_dv' -e 'def simulate' 'study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py' 'study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py'
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:17:def load_topology(filepath: str) -> tuple[list[str], dict[str, dict[str, int]]]:
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:41:class DVNode:
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:79:    def receive_dv(self, sender: str, dv: dict[str, float]) -> bool:
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:145:def simulate(topology_file: str) -> None:
```

## 3. 테스트와 남은 범위를 정리하기

마지막 단계에서는 단순히 테스트가 통과했다는 사실만 적지 않으려고 했다. 어디까지 확인됐고 무엇이 아직 범위 밖인지 같이 남겨야 글이 정직해진다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`를 다시 실행하고, `def test_convergence`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: 수렴 판정

핵심 코드/trace:

```python
def test_convergence(self):
        """DV를 교환하면 x에서 z까지 cost가 3(via y)로 수렴해야 한다."""
        x, y, z = self._make_triangle()

        # 한 round 동안 DV를 교환한다고 가정한다.
        dvs = {"x": x.get_dv(), "y": y.get_dv(), "z": z.get_dv()}

        x.receive_dv("y", dvs["y"])
        x.receive_dv("z", dvs["z"])
```

왜 이 코드가 중요했는가:

마지막에 이 파일을 남겨 두는 이유는, 이 프로젝트가 실제로 무엇을 통과해야 끝나는지 가장 직접적으로 보여 주기 때문이다.

CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/routing/problem test
TEST: 3-node topology convergence              [PASS]
TEST: x→z shortest path = 3 via y            [PASS]
TEST: 5-node topology convergence              [PASS]
TEST: a→e shortest path = 5                  [PASS]
 Results: 4 passed, 0 failed
```

## 남은 경계

- poisoned reverse는 구현하지 않았습니다.
- 동적 토폴로지 변화 실험은 포함하지 않습니다.
- 비동기 메시지 모델은 구현하지 않습니다.
