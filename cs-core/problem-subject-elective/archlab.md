# archlab 문제지

## 왜 중요한가

이 디렉터리는 Architecture Lab의 세 파트를 공식 문제 경계로 보존합니다. Part A는 Y86-64 어셈블리, Part B는 iaddq 제어 로직, Part C는 ncopy 성능 최적화에 해당합니다.

## 목표

시작 위치의 구현을 완성해 공식 self-study handout 복원 경로가 필요한 학습자, y86/ hand-in 산출물과 복원 toolchain의 관계를 알고 싶은 사람, 공개 가능한 파일과 로컬 전용 자산을 구분하고 싶은 사람을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Foundations-CSAPP/archlab/c/src/main.c`
- `../study/Foundations-CSAPP/archlab/c/src/mini_archlab.c`
- `../study/Foundations-CSAPP/archlab/cpp/src/main.cpp`
- `../study/Foundations-CSAPP/archlab/cpp/src/mini_archlab.cpp`
- `../study/Foundations-CSAPP/archlab/c/tests/test_mini_archlab.c`
- `../study/Foundations-CSAPP/archlab/cpp/tests/test_mini_archlab.cpp`
- `../study/Foundations-CSAPP/archlab/c/Makefile`
- `../study/Foundations-CSAPP/archlab/cpp/Makefile`

## starter code / 입력 계약

- `../study/Foundations-CSAPP/archlab/c/src/main.c`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 공식 self-study handout 복원 경로가 필요한 학습자
- y86/ hand-in 산출물과 복원 toolchain의 관계를 알고 싶은 사람
- 공개 가능한 파일과 로컬 전용 자산을 구분하고 싶은 사람
- 공식 toolchain과 템플릿은 problem/official/ 아래 로컬에서만 복원합니다.

## 제외 범위

- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`와 `arch_sum_list`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `expect_true`와 `expect_equal_ll`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/c test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/archlab/problem
```

- `archlab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`archlab_answer.md`](archlab_answer.md)에서 확인한다.
