# Scheduling Simulator 재구성 개발 로그

`scheduling-simulator`는 단일 CPU 위에서 scheduling policy가 waiting time, response time, turnaround time을 어떻게 바꾸는지 replay와 지표로 보여 주는 실험이다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

workload fixture와 공통 시뮬레이션 루프를 먼저 세운 뒤, policy별 차이가 replay/metric으로 어떻게 보이는지 따라간다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: fixture loader와 공통 simulation loop를 먼저 고정한다 — `python/src/os_scheduling/core.py`
- Phase 2: policy-specific helper로 fairness와 latency trade-off를 드러낸다 — `python/src/os_scheduling/core.py`
- Phase 3: replay 출력과 summary metric으로 실험을 닫는다 — `python/src/os_scheduling/cli.py`, `python/tests/test_os_scheduling.py`

## Phase 1. fixture loader와 공통 simulation loop를 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 policy 비교는 scheduler 함수보다 먼저 workload를 어떻게 읽고 timeline으로 돌릴지를 정해야 한다.

처음에는 FCFS/SJF/RR/MLFQ를 바로 구현하기보다 arrival/ready queue/metric 수집을 공통 루프로 빼는 편이 나중에 비교가 쉬울 것이라고 봤다. 그런데 실제로 글의 중심이 된 조치는 `load_fixture`, `simulate_policy`, arrival enqueue helper를 중심으로 공통 골격을 먼저 세웠다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_scheduling/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 공통 루프가 먼저 있기 때문에 각 policy 차이를 좁은 범위에서 설명할 수 있다.

### 이 장면을 고정하는 코드 — `load_fixture` (`python/src/os_scheduling/core.py:67`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```python
def load_fixture(path: str | Path) -> list[ProcessSpec]:
    data = json.loads(Path(path).read_text())
    specs = [ProcessSpec(**item) for item in data]
    for spec in specs:
        if spec.arrival < 0 or spec.burst <= 0:
            raise ValueError("arrival must be >= 0 and burst must be > 0")
    return specs
```

`load_fixture`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 scheduler 실험의 핵심은 policy 이름이 아니라 모두가 같은 workload 위에서 돌고 있다는 사실을 보존하는 데 있었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 policy별 분기와 metric 차이를 해석한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 scheduler 실험의 핵심은 policy 이름이 아니라 모두가 같은 workload 위에서 돌고 있다는 사실을 보존하는 데 있었다.

그래서 다음 장면에서는 policy별 분기와 metric 차이를 해석한다.

## Phase 2. policy-specific helper로 fairness와 latency trade-off를 드러낸다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `_simulate_fcfs`, `_simulate_sjf`, `_simulate_rr`, `_simulate_mlfq`와 queue helper가 실제 비교 지점을 만든다.

처음에는 policy 차이는 결과 표 하나보다 queue 조작 방식과 preemption 규칙이 어떻게 다른지에서 더 선명하게 드러날 것이라고 판단했다. 그런데 실제로 글의 중심이 된 조치는 policy별 시뮬레이터를 분리하고, boost/quantum/level pick helper를 두어 MLFQ의 고유 규칙을 명확히 했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_scheduling/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: policy helper가 분리돼 있어 metric 차이를 코드 수준에서 역추적할 수 있다.

### 이 장면을 고정하는 코드 — `_simulate_fcfs` (`python/src/os_scheduling/core.py:92`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```python
def _simulate_fcfs(states: list[ProcessState]) -> list[str]:
    pending = sorted(states, key=lambda item: (item.arrival, item.pid))
    ready: Deque[ProcessState] = deque()
    time = 0
    timeline: list[str] = []
```

`_simulate_fcfs`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 scheduler 설명은 알고리즘 이름보다 workload를 다시 어떻게 큐에 넣는지로 읽힐 때 훨씬 이해하기 쉬웠다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 replay CLI와 metrics 표로 결과를 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 scheduler 설명은 알고리즘 이름보다 workload를 다시 어떻게 큐에 넣는지로 읽힐 때 훨씬 이해하기 쉬웠다.

그래서 다음 장면에서는 replay CLI와 metrics 표로 결과를 닫는다.

## Phase 3. replay 출력과 summary metric으로 실험을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 scheduler lab은 내부 자료구조보다 replay와 평균 지표가 외부에서 읽히는지가 중요하다.

처음에는 CLI가 없다면 policy 차이를 설명하는 글이 결국 표 하나로 축약될 것 같아 replay surface를 끝까지 남겼다. 그런데 실제로 글의 중심이 된 조치는 `--replay` CLI와 `make run-demo`를 통해 timeline과 waiting/response/turnaround 표를 동시에 출력하게 했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_scheduling/cli.py`, `python/tests/test_os_scheduling.py`
- CLI: `make test && make run-demo`
- 검증 신호: 현재 demo 출력이 네 policy 차이를 한 번에 보여 준다.

### 이 장면을 고정하는 코드 — `main` (`python/src/os_scheduling/cli.py:21`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```python
def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    specs = load_fixture(args.fixture)
    policies = POLICIES if args.policy == "all" else (args.policy,)
    results = [simulate_policy(policy, specs) for policy in policies]
    if args.replay:
        for result in results:
            print(f"[{result.policy}]")
            print(render_replay(result))
    print(render_summary(results))
    return 0
```

`main`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 os 실험은 이론 요약보다 동일한 fixture를 policy별로 다시 재생하는 출력이 있을 때 가장 설득력이 컸다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 common loop -> policy helper -> replay metric 순서로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 OS 실험은 이론 요약보다 동일한 fixture를 policy별로 다시 재생하는 출력이 있을 때 가장 설득력이 컸다.

그래서 다음 장면에서는 common loop -> policy helper -> replay metric 순서로 닫는다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/scheduling-simulator/problem && make test && make run-demo)
```

```text
00-01:P1 | 02-03:P2 | 04-05:P3 | 06-07:P1 | 08-09:P2 | 10-13:P1
[mlfq]
00-00:P1 | 01-01:P2 | 02-02:P3 | 03-04:P1 | 05-06:P2 | 07-07:P3 | 08-11:P1 | 12-12:P2 | 13-13:P1
policy waiting response turnaround
 fcfs    6.67     6.67      11.33
  sjf    2.67     2.67       7.33
   rr    5.33      2.0       10.0
 mlfq     7.0      1.0      11.67
```

## 이번에 남은 질문

- 개념 축: `mlfq heuristics`, `policy tradeoffs`, `scheduler metrics`
- 대표 테스트/fixture: `python/tests/test_os_scheduling.py`
- 다음 질문: 최종 글은 common loop -> policy helper -> replay metric 순서로 닫는다.
