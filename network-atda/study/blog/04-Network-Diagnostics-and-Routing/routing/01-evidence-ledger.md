# Distance-Vector Routing evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 실행 표면과 entrypoint를 먼저 고정하기

- 당시 목표: `Distance-Vector Routing`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/routing/problem/README.md`, `study/04-Network-Diagnostics-and-Routing/routing/problem/Makefile`, `study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`
- 무슨 판단을 했는가: 문제 설명보다 실행 표면을 먼저 잡아야 뒤 설명이 흔들리지 않는다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/routing/problem help
  run-sim              Run the skeleton DV simulation
  run-solution         Run the solution DV simulation
  test                 Run the test script
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 진단 도구 이후에 네트워크 경로 계산 원리를 알고리즘 수준에서 다루는 단계로 자연스럽게 이어집니다.
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`의 `def load_topology`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. Bellman-Ford 갱신을 node 단위 상태 변화로 읽기

- 당시 목표: `Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`
- 무슨 판단을 했는가: 중심 규칙은 넓게 흩어져 있지 않고, 실제 분기나 frame evidence가 모이는 지점에 있다고 봤다.
- 실행한 CLI:

```bash
$ rg -n -e 'def load_topology' -e 'class DVNode' -e 'def receive_dv' -e 'def simulate' 'study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py' 'study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py'
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:17:def load_topology(filepath: str) -> tuple[list[str], dict[str, dict[str, int]]]:
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:41:class DVNode:
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:79:    def receive_dv(self, sender: str, dv: dict[str, float]) -> bool:
study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py:145:def simulate(topology_file: str) -> None:
```
- 검증 신호:
  - 이 출력만으로도 `def receive_dv` 주변이 설명의 중심축이라는 점이 드러난다.
  - 2-phase synchronous simulation
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/routing/python/src/dv_routing.py`의 `def receive_dv`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. 테스트와 남은 범위를 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 검증 출력이 좋게 나와도 README limitation을 그대로 남겨야 범위가 정확해진다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/04-Network-Diagnostics-and-Routing/routing/problem test
TEST: 3-node topology convergence              [PASS]
TEST: x→z shortest path = 3 via y            [PASS]
TEST: 5-node topology convergence              [PASS]
TEST: a→e shortest path = 5                  [PASS]
 Results: 4 passed, 0 failed
```
- 검증 신호:
  - `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - poisoned reverse는 구현하지 않았습니다.
- 핵심 코드/trace 앵커: `study/04-Network-Diagnostics-and-Routing/routing/python/tests/test_dv_routing.py`의 `def test_convergence`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
