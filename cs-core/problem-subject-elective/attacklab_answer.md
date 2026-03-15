# attacklab 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 공개 self-study target을 로컬에 복원해 보고 싶은 학습자, 문제 계약과 companion verifier의 경계를 나눠 보고 싶은 사람, 보안 과제 공개 범위를 안전하게 관리하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `hex_value`, `read_u64_le` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 공개 self-study target을 로컬에 복원해 보고 싶은 학습자
- 문제 계약과 companion verifier의 경계를 나눠 보고 싶은 사람
- 보안 과제 공개 범위를 안전하게 관리하고 싶은 사람
- 첫 진입점은 `../study/Foundations-CSAPP/attacklab/c/src/main.c`이고, 여기서 `main`와 `hex_value` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Foundations-CSAPP/attacklab/c/src/main.c`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/attacklab/c/src/mini_attacklab.c`: `hex_value`, `read_u64_le`, `matches_u64_le`, `parse_hex_string`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/attacklab/cpp/src/main.cpp`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/attacklab/cpp/src/mini_attacklab.cpp`: `hex_value`, `matches_u64_le`, `prefix_matches`, `tail_matches`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/attacklab/problem/code/farm.c`: `setval_210`, `setval_426`, `getval_280`, `getval_481`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/attacklab/c/tests/test_mini_attacklab.c`: `expect_true`, `expect_false`, `parse`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/attacklab/cpp/tests/test_mini_attacklab.cpp`: `expect_true`, `expect_false`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/attacklab/c/data/phase1.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/Foundations-CSAPP/attacklab/problem/code/farm.c`와 `../study/Foundations-CSAPP/attacklab/c/src/main.c`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `expect_true` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/attacklab/c test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/attacklab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/attacklab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/attacklab/problem
```

- `../study/Foundations-CSAPP/attacklab/problem/code/farm.c` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `expect_true`와 `expect_false`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/attacklab/c test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Foundations-CSAPP/attacklab/c/src/main.c`
- `../study/Foundations-CSAPP/attacklab/c/src/mini_attacklab.c`
- `../study/Foundations-CSAPP/attacklab/cpp/src/main.cpp`
- `../study/Foundations-CSAPP/attacklab/cpp/src/mini_attacklab.cpp`
- `../study/Foundations-CSAPP/attacklab/problem/code/farm.c`
- `../study/Foundations-CSAPP/attacklab/c/tests/test_mini_attacklab.c`
- `../study/Foundations-CSAPP/attacklab/cpp/tests/test_mini_attacklab.cpp`
- `../study/Foundations-CSAPP/attacklab/c/data/phase1.txt`
- `../study/Foundations-CSAPP/attacklab/c/data/phase2.txt`
- `../study/Foundations-CSAPP/attacklab/c/data/phase3.txt`
