# perflab 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 구현 전에 문제 계약과 제공 파일을 먼저 보고 싶은 학습자, 공식 자산 없이도 공개 가능한 starter boundary를 만들고 싶은 사람, sample trace와 driver의 역할을 알고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 `print_trace_result`와 `print_transpose_result`, `main` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 구현 전에 문제 계약과 제공 파일을 먼저 보고 싶은 학습자
- 공식 자산 없이도 공개 가능한 starter boundary를 만들고 싶은 사람
- sample trace와 driver의 역할을 알고 싶은 사람
- 첫 진입점은 `../study/Foundations-CSAPP/perflab/c/src/main.c`이고, 여기서 `print_trace_result`와 `print_transpose_result` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Foundations-CSAPP/perflab/c/src/main.c`: `print_trace_result`, `print_transpose_result`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/perflab/c/src/perflab.c`: `cache_sim_init`, `cache_sim_destroy`, `cache_access`, `perflab_run_trace_file`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/perflab/cpp/src/main.cpp`: `print_trace_result`, `print_transpose_result`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/perflab/cpp/src/perflab.cpp`: `cache_sim_init`, `cache_access`, `transpose_cache_init`, `transpose_access`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.c`: `printSummary`, `registerTransFunction`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.h`: `printSummary`, `void`, `registerTransFunction`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/perflab/c/tests/test_perflab.c`: `expect_equal_int`, `expect_true`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/perflab/cpp/tests/test_perflab.cpp`: `expect_equal_int`, `expect_true`, `main`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/Foundations-CSAPP/perflab/problem/code/cachelab.c`와 `../study/Foundations-CSAPP/perflab/c/src/main.c`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `expect_equal_int` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/c test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/problem
```

- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.c` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `expect_equal_int`와 `expect_true`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/c test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Foundations-CSAPP/perflab/c/src/main.c`
- `../study/Foundations-CSAPP/perflab/c/src/perflab.c`
- `../study/Foundations-CSAPP/perflab/cpp/src/main.cpp`
- `../study/Foundations-CSAPP/perflab/cpp/src/perflab.cpp`
- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.c`
- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.h`
- `../study/Foundations-CSAPP/perflab/c/tests/test_perflab.c`
- `../study/Foundations-CSAPP/perflab/cpp/tests/test_perflab.cpp`
- `../study/Foundations-CSAPP/perflab/problem/csim-starter.dSYM/Contents/Resources/Relocations/aarch64/csim-starter.yml`
- `../study/Foundations-CSAPP/perflab/problem/data/traces/study.trace`
