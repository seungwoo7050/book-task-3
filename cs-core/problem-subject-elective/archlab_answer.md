# archlab 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 공식 self-study handout 복원 경로가 필요한 학습자, y86/ hand-in 산출물과 복원 toolchain의 관계를 알고 싶은 사람, 공개 가능한 파일과 로컬 전용 자산을 구분하고 싶은 사람을 한 흐름으로 설명하고 검증한다. 핵심은 `main`와 `arch_sum_list`, `arch_rsum_list` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 공식 self-study handout 복원 경로가 필요한 학습자
- y86/ hand-in 산출물과 복원 toolchain의 관계를 알고 싶은 사람
- 공개 가능한 파일과 로컬 전용 자산을 구분하고 싶은 사람
- 첫 진입점은 `../study/Foundations-CSAPP/archlab/c/src/main.c`이고, 여기서 `main`와 `arch_sum_list` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Foundations-CSAPP/archlab/c/src/main.c`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/archlab/c/src/mini_archlab.c`: `arch_sum_list`, `arch_rsum_list`, `arch_copy_block`, `add_overflow`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/archlab/cpp/src/main.cpp`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/archlab/cpp/src/mini_archlab.cpp`: `add_overflow`, `seq_iaddq`, `ncopy_baseline`, `ncopy_optimized`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/archlab/c/include/mini_archlab.h`: `arch_sum_list`, `arch_rsum_list`, `arch_copy_block`, `arch_seq_iaddq`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Foundations-CSAPP/archlab/c/tests/test_mini_archlab.c`: `expect_true`, `expect_equal_ll`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/archlab/cpp/tests/test_mini_archlab.cpp`: `expect_true`, `expect_equal_ll`, `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Foundations-CSAPP/archlab/c/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/Foundations-CSAPP/archlab/c/src/main.c`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `expect_true` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/c test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/problem
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `expect_true`와 `expect_equal_ll`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/c test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Foundations-CSAPP/archlab/c/src/main.c`
- `../study/Foundations-CSAPP/archlab/c/src/mini_archlab.c`
- `../study/Foundations-CSAPP/archlab/cpp/src/main.cpp`
- `../study/Foundations-CSAPP/archlab/cpp/src/mini_archlab.cpp`
- `../study/Foundations-CSAPP/archlab/c/include/mini_archlab.h`
- `../study/Foundations-CSAPP/archlab/c/tests/test_mini_archlab.c`
- `../study/Foundations-CSAPP/archlab/cpp/tests/test_mini_archlab.cpp`
- `../study/Foundations-CSAPP/archlab/c/Makefile`
- `../study/Foundations-CSAPP/archlab/cpp/Makefile`
