# bomblab 문제지

## 왜 중요한가

이 디렉터리는 Bomb Lab의 공식 과제 계약과 공개 가능한 분석 경계를 보존합니다. 핵심은 주어진 x86-64 bomb를 무작정 brute force하지 않고 단계적으로 해석하는 것입니다.

## 목표

시작 위치의 구현을 완성해 공식 self-study bomb를 로컬에서 복원해 보고 싶은 학습자, 어떤 파일은 공개하고 어떤 자산은 제외해야 하는지 알고 싶은 사람, companion 구현과 공식 문제 경계를 분리해서 관리하고 싶은 사람을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Foundations-CSAPP/bomblab/problem/code/bomb.c`
- `../study/Foundations-CSAPP/bomblab/c/src/main.c`
- `../study/Foundations-CSAPP/bomblab/c/src/mini_bomb.c`
- `../study/Foundations-CSAPP/bomblab/cpp/src/main.cpp`
- `../study/Foundations-CSAPP/bomblab/cpp/src/mini_bomb.cpp`
- `../study/Foundations-CSAPP/bomblab/c/tests/test_mini_bomb.c`
- `../study/Foundations-CSAPP/bomblab/cpp/tests/test_mini_bomb.cpp`
- `../study/Foundations-CSAPP/bomblab/problem/data/solutions.txt`

## starter code / 입력 계약

- ../study/Foundations-CSAPP/bomblab/problem/code/bomb.c에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 공식 self-study bomb를 로컬에서 복원해 보고 싶은 학습자
- 어떤 파일은 공개하고 어떤 자산은 제외해야 하는지 알고 싶은 사람
- companion 구현과 공식 문제 경계를 분리해서 관리하고 싶은 사람
- script/run_bomb.sh

## 제외 범위

- `../study/Foundations-CSAPP/bomblab/problem/code/bomb.c` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Foundations-CSAPP/bomblab/problem/data/solutions.txt` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/Foundations-CSAPP/bomblab/problem/code/bomb.c`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `read_line`와 `validate_phase`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `expect_true`와 `expect_false`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Foundations-CSAPP/bomblab/problem/data/solutions.txt` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/problem test
```

- `bomblab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`bomblab_answer.md`](bomblab_answer.md)에서 확인한다.
