# perflab 문제지

## 왜 중요한가

이 디렉터리는 Performance Lab의 공식 starter boundary를 self-written 형태로 유지합니다. Part A는 trace-driven cache simulator, Part B는 cache-friendly transpose가 핵심입니다.

## 목표

시작 위치의 구현을 완성해 구현 전에 문제 계약과 제공 파일을 먼저 보고 싶은 학습자, 공식 자산 없이도 공개 가능한 starter boundary를 만들고 싶은 사람, sample trace와 driver의 역할을 알고 싶은 사람을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.c`
- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.h`
- `../study/Foundations-CSAPP/perflab/c/src/main.c`
- `../study/Foundations-CSAPP/perflab/c/src/perflab.c`
- `../study/Foundations-CSAPP/perflab/cpp/src/main.cpp`
- `../study/Foundations-CSAPP/perflab/cpp/src/perflab.cpp`
- `../study/Foundations-CSAPP/perflab/c/tests/test_perflab.c`
- `../study/Foundations-CSAPP/perflab/cpp/tests/test_perflab.cpp`

## starter code / 입력 계약

- ../study/Foundations-CSAPP/perflab/problem/code/cachelab.c에서 starter 코드와 입력 경계를 잡는다.
- ../study/Foundations-CSAPP/perflab/problem/code/cachelab.h에서 starter 코드와 입력 경계를 잡는다.
- ../study/Foundations-CSAPP/perflab/problem/code/csim.c에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 구현 전에 문제 계약과 제공 파일을 먼저 보고 싶은 학습자
- 공식 자산 없이도 공개 가능한 starter boundary를 만들고 싶은 사람
- sample trace와 driver의 역할을 알고 싶은 사람
- 공개 트리에는 self-written starter와 sample trace만 둡니다.

## 제외 범위

- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.c` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Foundations-CSAPP/perflab/problem/csim-starter.dSYM/Contents/Resources/Relocations/aarch64/csim-starter.yml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/Foundations-CSAPP/perflab/problem/code/cachelab.c`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `print_trace_result`와 `print_transpose_result`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `expect_equal_int`와 `expect_true`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/Foundations-CSAPP/perflab/problem/csim-starter.dSYM/Contents/Resources/Relocations/aarch64/csim-starter.yml` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/perflab/problem
```

- `perflab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`perflab_answer.md`](perflab_answer.md)에서 확인한다.
