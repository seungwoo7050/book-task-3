# Malloc Lab 문제 경계

## 이 디렉터리가 가르치는 것

이 디렉터리는 `mm_init`, `mm_malloc`, `mm_free`, `mm_realloc` 계약과 trace driver를 보존합니다.
핵심은 `memlib.c`가 제공하는 simulated heap만 사용해 allocator를 구현하는 것입니다.

## 누구를 위한 문서인가

- allocator API 계약을 먼저 확인하고 싶은 학습자
- trace 형식과 driver 역할을 이해하고 싶은 사람
- 구현 디렉터리와 문제 경계를 분리하고 싶은 사람

## 먼저 읽을 곳

1. [`../README.md`](../README.md)
2. [`../docs/README.md`](../docs/README.md)
3. `code/mm.h`
4. `data/traces/`

## 디렉터리 구조

```text
problem/
  README.md
  code/
    mm.c
    mm.h
    memlib.c
    memlib.h
  data/
    traces/
  script/
    mdriver.c
  Makefile
```

## 검증 방법

```bash
cd problem
make clean && make
```

구현 검증은 [`../c/README.md`](../c/README.md)와 [`../cpp/README.md`](../cpp/README.md)를 따릅니다.

## 스포일러 경계

- README는 API 계약, trace 형식, driver 역할만 설명합니다.
- 구체 allocator 정책은 구현 디렉터리와 `docs/`에 둡니다.

## 포트폴리오로 확장하는 힌트

- 문제 경계 README에 trace 형식을 남겨 두면 구현이 바뀌어도 저장소가 오래 살아남습니다.
