# scheduling-simulator 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 fixture가 policy별 deterministic timeline을 만든다, FCFS/SJF/RR/MLFQ 결과가 tests의 golden expectation과 일치한다, run-demo가 policy별 replay와 metrics table을 같은 shape로 출력한다를 한 흐름으로 설명하고 검증한다. 핵심은 `build_parser`와 `main`, `ProcessSpec` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- fixture가 policy별 deterministic timeline을 만든다.
- FCFS/SJF/RR/MLFQ 결과가 tests의 golden expectation과 일치한다.
- run-demo가 policy별 replay와 metrics table을 같은 shape로 출력한다.
- 첫 진입점은 `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__init__.py`이고, 여기서 `build_parser`와 `main` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__main__.py`: CLI나 demo 실행 순서를 묶는 진입점 파일이다.
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/cli.py`: `build_parser`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/core.py`: `ProcessSpec`, `ProcessState`, `ProcessMetric`, `PolicyResult`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Operating-Systems-Internals/scheduling-simulator/python/tests/test_os_scheduling.py`: `test_convoy_golden_timelines`, `test_sjf_reduces_waiting_time_on_convoy_fixture`, `test_rr_improves_response_time_on_convoy_fixture`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/convoy.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/interactive-mix.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_convoy_golden_timelines` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test && make run-demo`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make run-demo
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/scheduling-simulator/problem test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_convoy_golden_timelines`와 `test_sjf_reduces_waiting_time_on_convoy_fixture`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make run-demo`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__init__.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/__main__.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/cli.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/src/os_scheduling/core.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/python/tests/test_os_scheduling.py`
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/convoy.json`
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/data/interactive-mix.json`
- `../study/Operating-Systems-Internals/scheduling-simulator/problem/Makefile`
