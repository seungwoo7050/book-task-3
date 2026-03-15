# virtual-memory-lab-python 문제지

## 왜 중요한가

trace 형식은 줄 단위 <R|W> <page>로 고정한다. page replacement policy는 FIFO, LRU, Clock, OPT로 고정한다. frame 수와 trace가 주어졌을 때 hits, faults, dirty evictions를 계산한다. replay는 각 접근 뒤 frame 상태를 표 형태로 출력한다.

## 목표

시작 위치의 구현을 완성해 classic Belady anomaly 예제가 FIFO에서 재현된다, locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다, dirty trace에서 dirty eviction이 정확히 계산된다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__init__.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__main__.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/cli.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/core.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/tests/test_os_virtual_memory.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/belady.trace`
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/dirty.trace`
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/locality.trace`

## starter code / 입력 계약

- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- classic Belady anomaly 예제가 FIFO에서 재현된다.
- locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다.
- dirty trace에서 dirty eviction이 정확히 계산된다.

## 제외 범위

- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/belady.trace` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `build_parser`와 `main`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_fifo_belady_anomaly`와 `test_locality_trace_favors_lru_and_opt`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/belady.trace` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test && make run-demo`가 통과한다.

## 검증 방법

```bash
make test && make run-demo
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/virtual-memory-lab/python && PYTHONPATH=src python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/virtual-memory-lab/problem test
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`virtual-memory-lab-python_answer.md`](virtual-memory-lab-python_answer.md)에서 확인한다.
