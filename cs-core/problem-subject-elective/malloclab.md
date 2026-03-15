# malloclab 문제지

## 왜 중요한가

이 디렉터리는 mm_init, mm_malloc, mm_free, mm_realloc 계약과 trace driver를 보존합니다. 핵심은 memlib.c가 제공하는 simulated heap만 사용해 allocator를 구현하는 것입니다.

## 목표

시작 위치의 구현을 완성해 allocator API 계약을 먼저 확인하고 싶은 학습자, trace 형식과 driver 역할을 이해하고 싶은 사람, 구현 디렉터리와 문제 경계를 분리하고 싶은 사람을 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/Systems-Programming/malloclab/problem/code/memlib.c`
- `../study/Systems-Programming/malloclab/problem/code/memlib.h`
- `../study/Systems-Programming/malloclab/c/src/mm.c`
- `../study/Systems-Programming/malloclab/cpp/src/mm.cpp`
- `../study/Systems-Programming/malloclab/problem/data/traces/basic.rep`
- `../study/Systems-Programming/malloclab/problem/data/traces/coalesce.rep`
- `../study/Systems-Programming/malloclab/problem/data/traces/mixed.rep`
- `../study/Systems-Programming/malloclab/c/Makefile`

## starter code / 입력 계약

- ../study/Systems-Programming/malloclab/problem/code/memlib.c에서 starter 코드와 입력 경계를 잡는다.
- ../study/Systems-Programming/malloclab/problem/code/memlib.h에서 starter 코드와 입력 경계를 잡는다.
- ../study/Systems-Programming/malloclab/problem/code/mm.c에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- allocator API 계약을 먼저 확인하고 싶은 학습자
- trace 형식과 driver 역할을 이해하고 싶은 사람
- 구현 디렉터리와 문제 경계를 분리하고 싶은 사람
- code/mm.h

## 제외 범위

- `../study/Systems-Programming/malloclab/problem/code/memlib.c` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/Systems-Programming/malloclab/problem/data/traces/basic.rep` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/Systems-Programming/malloclab/problem/code/memlib.c`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `align_size`와 `pack`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- `../study/Systems-Programming/malloclab/problem/data/traces/basic.rep` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/c test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/c test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/cpp test
```

```bash
make -C /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/malloclab/problem
```

- `malloclab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`malloclab_answer.md`](malloclab_answer.md)에서 확인한다.
