# bomblab 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 공식 self-study bomb를 로컬에서 복원해 보고 싶은 학습자, 어떤 파일은 공개하고 어떤 자산은 제외해야 하는지 알고 싶은 사람, companion 구현과 공식 문제 경계를 분리해서 관리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 `read_line`와 `validate_phase`, `main` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 공식 self-study bomb를 로컬에서 복원해 보고 싶은 학습자
- 어떤 파일은 공개하고 어떤 자산은 제외해야 하는지 알고 싶은 사람
- companion 구현과 공식 문제 경계를 분리해서 관리하고 싶은 사람
- 첫 진입점은 `../study/Foundations-CSAPP/bomblab/c/src/main.c`이고, 여기서 `read_line`와 `validate_phase` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Foundations-CSAPP/bomblab/c/src/main.c`: `read_line`, `validate_phase`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/bomblab/c/src/mini_bomb.c`: `parse_two_ints`, `parse_one_int`, `parse_six_ints`, `phase3_expected`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/bomblab/cpp/src/main.cpp`: `validate_phase`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/bomblab/cpp/src/mini_bomb.cpp`: `parse_exact_ints`, `phase3_expected`, `func4`, `reset_nodes`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/bomblab/problem/code/bomb.c`: `initialize_bomb`, `phase_1`, `phase_2`, `phase_3`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/bomblab/c/tests/test_mini_bomb.c`: `expect_true`, `expect_false`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/bomblab/cpp/tests/test_mini_bomb.cpp`: `expect_true`, `expect_false`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/bomblab/problem/data/solutions.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/Foundations-CSAPP/bomblab/problem/code/bomb.c`와 `../study/Foundations-CSAPP/bomblab/c/src/main.c`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `expect_true` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/c test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/problem test
```

- `../study/Foundations-CSAPP/bomblab/problem/code/bomb.c` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `expect_true`와 `expect_false`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/c test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Foundations-CSAPP/bomblab/c/src/main.c`
- `../study/Foundations-CSAPP/bomblab/c/src/mini_bomb.c`
- `../study/Foundations-CSAPP/bomblab/cpp/src/main.cpp`
- `../study/Foundations-CSAPP/bomblab/cpp/src/mini_bomb.cpp`
- `../study/Foundations-CSAPP/bomblab/problem/code/bomb.c`
- `../study/Foundations-CSAPP/bomblab/c/tests/test_mini_bomb.c`
- `../study/Foundations-CSAPP/bomblab/cpp/tests/test_mini_bomb.cpp`
- `../study/Foundations-CSAPP/bomblab/problem/data/solutions.txt`
- `../study/Foundations-CSAPP/bomblab/problem/script/run_bomb.sh`
- `../study/Foundations-CSAPP/bomblab/c/Makefile`
