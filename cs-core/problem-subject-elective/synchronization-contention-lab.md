# synchronization-contention-lab 문제지

## 왜 중요한가

counter 시나리오는 mutex로 shared counter를 보호한다. gate 시나리오는 POSIX semaphore로 동시 진입 수를 제한한다. buffer 시나리오는 mutex + condition variable로 bounded buffer를 보호한다. 출력은 timing보다 correctness invariant를 우선 보고, elapsed time과 wait count는 보조 지표로만 기록한다.

## 목표

시작 위치의 구현을 완성해 counter final count가 expected count와 일치한다, semaphore gate의 max concurrency가 permit limit를 넘지 않는다, bounded buffer에서 underflow/overflow 없이 생산량과 소비량이 일치한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/contention_lab.c`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/main.c`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/include/contention_lab.h`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/tests/test_cases.sh`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/Makefile`
- `../study/Operating-Systems-Internals/synchronization-contention-lab/problem/Makefile`

## starter code / 입력 계약

- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/src/contention_lab.c`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- counter final count가 expected count와 일치한다.
- semaphore gate의 max concurrency가 permit limit를 넘지 않는다.
- bounded buffer에서 underflow/overflow 없이 생산량과 소비량이 일치한다.

## 제외 범위

- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/tests/test_cases.sh` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `elapsed_ms`와 `run_counter_scenario`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- `../study/Operating-Systems-Internals/synchronization-contention-lab/c/tests/test_cases.sh` fixture/trace 기준으로 결과를 대조했다.
- `make test && make run-demo`가 통과한다.

## 검증 방법

```bash
make test && make run-demo
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/problem test
```

- `synchronization-contention-lab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`synchronization-contention-lab_answer.md`](synchronization-contention-lab_answer.md)에서 확인한다.
