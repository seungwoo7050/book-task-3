# scheduling-simulator 문제지

## 왜 중요한가

입력 fixture는 JSON 배열 [{ "pid": "...", "arrival": <int>, "burst": <int> }] 형식으로 고정한다. 단일 CPU, 정수 tick, 단일 CPU burst만 다룬다. FCFS, non-preemptive SJF, RR(quantum 2), MLFQ(3 queues, quanta 1/2/4, dispatch-boundary boost 10 ticks)를 구현한다. 정책별 평균 waiting time, response time, turnaround time과 ASCII replay를 출력한다.

## 목표

시작 위치의 구현을 완성해 fixture가 policy별 deterministic timeline을 만든다, FCFS/SJF/RR/MLFQ 결과가 tests의 golden expectation과 일치한다, run-demo가 policy별 replay와 metrics table을 같은 shape로 출력한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__init__.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__main__.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/cli.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/core.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/tests/test_os_scheduling.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/convoy.json`
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/interactive-mix.json`
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/Makefile`

## starter code / 입력 계약

- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- fixture가 policy별 deterministic timeline을 만든다.
- FCFS/SJF/RR/MLFQ 결과가 tests의 golden expectation과 일치한다.
- run-demo가 policy별 replay와 metrics table을 같은 shape로 출력한다.

## 제외 범위

- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/convoy.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `build_parser`와 `main`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_convoy_golden_timelines`와 `test_sjf_reduces_waiting_time_on_convoy_fixture`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/convoy.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test && make run-demo`가 통과한다.

## 검증 방법

```bash
make test && make run-demo
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/scheduling-simulator/problem test
```

- `scheduling-simulator`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`scheduling-simulator_answer.md`](scheduling-simulator_answer.md)에서 확인한다.
