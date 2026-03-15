# virtual-memory-lab-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 classic Belady anomaly 예제가 FIFO에서 재현된다, locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다, dirty trace에서 dirty eviction이 정확히 계산된다를 한 흐름으로 설명하고 검증한다. 핵심은 `build_parser`와 `main`, `PageAccess` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- classic Belady anomaly 예제가 FIFO에서 재현된다.
- locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다.
- dirty trace에서 dirty eviction이 정확히 계산된다.
- 첫 진입점은 `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__init__.py`이고, 여기서 `build_parser`와 `main` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__main__.py`: CLI나 demo 실행 순서를 묶는 진입점 파일이다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/cli.py`: `build_parser`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/core.py`: `PageAccess`, `Frame`, `ReplayStep`, `PolicyResult`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/tests/test_os_virtual_memory.py`: `test_fifo_belady_anomaly`, `test_locality_trace_favors_lru_and_opt`, `test_dirty_evictions_counted`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/belady.trace`: 핵심 구현을 담는 파일이다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/dirty.trace`: 핵심 구현을 담는 파일이다.
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/locality.trace`: 핵심 구현을 담는 파일이다.

## 정답을 재구성하는 절차

1. `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_fifo_belady_anomaly` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test && make run-demo`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make run-demo
```

```bash
cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/virtual-memory-lab/python && PYTHONPATH=src python3 -m pytest
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/virtual-memory-lab/problem test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_fifo_belady_anomaly`와 `test_locality_trace_favors_lru_and_opt`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make run-demo`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__init__.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/__main__.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/cli.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/src/os_virtual_memory/core.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/python/tests/test_os_virtual_memory.py`
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/belady.trace`
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/dirty.trace`
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/data/locality.trace`
- `../study/Operating-Systems-Internals/virtual-memory-lab/problem/Makefile`
