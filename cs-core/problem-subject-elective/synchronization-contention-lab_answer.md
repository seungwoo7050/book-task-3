# synchronization-contention-lab 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 counter final count가 expected count와 일치한다, semaphore gate의 max concurrency가 permit limit를 넘지 않는다, bounded buffer에서 underflow/overflow 없이 생산량과 소비량이 일치한다를 한 흐름으로 설명하고 검증한다. 핵심은 `elapsed_ms`와 `run_counter_scenario`, `run_gate_scenario` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- counter final count가 expected count와 일치한다.
- semaphore gate의 max concurrency가 permit limit를 넘지 않는다.
- bounded buffer에서 underflow/overflow 없이 생산량과 소비량이 일치한다.
- 첫 진입점은 `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/contention_lab.c`이고, 여기서 `elapsed_ms`와 `run_counter_scenario` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/contention_lab.c`: `elapsed_ms`, `run_counter_scenario`, `run_gate_scenario`, `run_buffer_scenario`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/main.c`: `usage`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/include/contention_lab.h`: `run_counter_scenario`, `run_gate_scenario`, `run_buffer_scenario`, `print_metrics`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/tests/test_cases.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `../study/Operating-Systems-Internals/synchronization-contention-lab/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `elapsed_ms` 등이 맡는 책임을 한 함수에 뭉개지 말고 상태 전이 단위로 분리한다.
- 회귀 게이트는 `make test && make run-demo`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.

## 정답을 재구성하는 절차

1. `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/contention_lab.c`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `elapsed_ms` 등이 맡는 책임을 분리해 각 출력 계약을 완성한다.
3. `make test && make run-demo`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make run-demo
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/problem test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/tests/test_cases.sh` fixture/trace를 읽지 않고 동작을 추측하지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make run-demo`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/contention_lab.c`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/main.c`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/include/contention_lab.h`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/tests/test_cases.sh`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/Makefile`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/problem/Makefile`
