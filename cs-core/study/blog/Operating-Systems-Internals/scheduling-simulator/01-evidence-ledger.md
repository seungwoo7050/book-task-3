# Scheduling Simulator Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`scheduling-simulator`는 단일 CPU 위에서 scheduling policy가 waiting time, response time, turnaround time을 어떻게 바꾸는지 replay와 지표로 보여 주는 실험이다. 구현의 중심은 `python`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `python/src/os_scheduling/__init__.py`, `python/src/os_scheduling/__main__.py`, `python/src/os_scheduling/cli.py`, `python/src/os_scheduling/core.py`다. 검증 표면은 `python/tests/test_os_scheduling.py`와 `make test && make run-demo`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `mlfq heuristics`, `policy tradeoffs`, `scheduler metrics`이다.

## Git History Anchor

- `2026-03-11	0cccd64	feat: add new project in cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - fixture loader와 공통 simulation loop를 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 policy 비교는 scheduler 함수보다 먼저 workload를 어떻게 읽고 timeline으로 돌릴지를 정해야 한다.

그때 세운 가설은 FCFS/SJF/RR/MLFQ를 바로 구현하기보다 arrival/ready queue/metric 수집을 공통 루프로 빼는 편이 나중에 비교가 쉬울 것이라고 봤다. 실제 조치는 `load_fixture`, `simulate_policy`, arrival enqueue helper를 중심으로 공통 골격을 먼저 세웠다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_scheduling/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 공통 루프가 먼저 있기 때문에 각 policy 차이를 좁은 범위에서 설명할 수 있다.
- 새로 배운 것: scheduler 실험의 핵심은 policy 이름이 아니라 모두가 같은 workload 위에서 돌고 있다는 사실을 보존하는 데 있었다.

### 코드 앵커 — `load_fixture` (`python/src/os_scheduling/core.py:67`)

```python
def load_fixture(path: str | Path) -> list[ProcessSpec]:
    data = json.loads(Path(path).read_text())
    specs = [ProcessSpec(**item) for item in data]
    for spec in specs:
        if spec.arrival < 0 or spec.burst <= 0:
            raise ValueError("arrival must be >= 0 and burst must be > 0")
    return specs
```

이 조각은 공통 루프가 먼저 있기 때문에 각 policy 차이를 좁은 범위에서 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `load_fixture`를 읽고 나면 다음 장면이 왜 policy별 분기와 metric 차이를 해석한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `simulate_policy` (`python/src/os_scheduling/core.py:76`)

```python
def simulate_policy(policy: str, specs: Iterable[ProcessSpec]) -> PolicyResult:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")
    states = [ProcessState.from_spec(spec) for spec in specs]
    if policy == "fcfs":
        timeline = _simulate_fcfs(states)
    elif policy == "sjf":
        timeline = _simulate_sjf(states)
    elif policy == "rr":
        timeline = _simulate_rr(states, quantum=2)
    else:
        timeline = _simulate_mlfq(states, quanta=(1, 2, 4), boost_interval=10)
```

이 조각은 공통 루프가 먼저 있기 때문에 각 policy 차이를 좁은 범위에서 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `simulate_policy`를 읽고 나면 다음 장면이 왜 policy별 분기와 metric 차이를 해석한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 policy별 분기와 metric 차이를 해석한다.

## 2. Phase 2 - policy-specific helper로 fairness와 latency trade-off를 드러낸다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `_simulate_fcfs`, `_simulate_sjf`, `_simulate_rr`, `_simulate_mlfq`와 queue helper가 실제 비교 지점을 만든다.

그때 세운 가설은 policy 차이는 결과 표 하나보다 queue 조작 방식과 preemption 규칙이 어떻게 다른지에서 더 선명하게 드러날 것이라고 판단했다. 실제 조치는 policy별 시뮬레이터를 분리하고, boost/quantum/level pick helper를 두어 MLFQ의 고유 규칙을 명확히 했다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_scheduling/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: policy helper가 분리돼 있어 metric 차이를 코드 수준에서 역추적할 수 있다.
- 새로 배운 것: scheduler 설명은 알고리즘 이름보다 workload를 다시 어떻게 큐에 넣는지로 읽힐 때 훨씬 이해하기 쉬웠다.

### 코드 앵커 — `_simulate_fcfs` (`python/src/os_scheduling/core.py:92`)

```python
def _simulate_fcfs(states: list[ProcessState]) -> list[str]:
    pending = sorted(states, key=lambda item: (item.arrival, item.pid))
    ready: Deque[ProcessState] = deque()
    time = 0
    timeline: list[str] = []
```

이 조각은 policy helper가 분리돼 있어 metric 차이를 코드 수준에서 역추적할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `_simulate_fcfs`를 읽고 나면 다음 장면이 왜 replay CLI와 metrics 표로 결과를 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `_simulate_sjf` (`python/src/os_scheduling/core.py:113`)

```python
def _simulate_sjf(states: list[ProcessState]) -> list[str]:
    pending = sorted(states, key=lambda item: (item.arrival, item.pid))
    ready: list[ProcessState] = []
    time = 0
    timeline: list[str] = []
```

이 조각은 policy helper가 분리돼 있어 metric 차이를 코드 수준에서 역추적할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `_simulate_sjf`를 읽고 나면 다음 장면이 왜 replay CLI와 metrics 표로 결과를 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 replay CLI와 metrics 표로 결과를 닫는다.

## 3. Phase 3 - replay 출력과 summary metric으로 실험을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 scheduler lab은 내부 자료구조보다 replay와 평균 지표가 외부에서 읽히는지가 중요하다.

그때 세운 가설은 CLI가 없다면 policy 차이를 설명하는 글이 결국 표 하나로 축약될 것 같아 replay surface를 끝까지 남겼다. 실제 조치는 `--replay` CLI와 `make run-demo`를 통해 timeline과 waiting/response/turnaround 표를 동시에 출력하게 했다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_scheduling/cli.py`, `python/tests/test_os_scheduling.py`
- CLI: `make test && make run-demo`
- 검증 신호: 현재 demo 출력이 네 policy 차이를 한 번에 보여 준다.
- 새로 배운 것: OS 실험은 이론 요약보다 동일한 fixture를 policy별로 다시 재생하는 출력이 있을 때 가장 설득력이 컸다.

### 코드 앵커 — `main` (`python/src/os_scheduling/cli.py:21`)

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

이 조각은 현재 demo 출력이 네 policy 차이를 한 번에 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `main`를 읽고 나면 다음 장면이 왜 common loop -> policy helper -> replay metric 순서로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `test_sjf_reduces_waiting_time_on_convoy_fixture` (`python/tests/test_os_scheduling.py:80`)

```python
def test_sjf_reduces_waiting_time_on_convoy_fixture() -> None:
    specs = load_fixture(FIXTURE_DIR / "convoy.json")
    fcfs = simulate_policy("fcfs", specs)
    sjf = simulate_policy("sjf", specs)
    assert sjf.averages["waiting"] < fcfs.averages["waiting"]
```

이 조각은 현재 demo 출력이 네 policy 차이를 한 번에 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `test_sjf_reduces_waiting_time_on_convoy_fixture`를 읽고 나면 다음 장면이 왜 common loop -> policy helper -> replay metric 순서로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 common loop -> policy helper -> replay metric 순서로 닫는다.

## Latest CLI Excerpt

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
