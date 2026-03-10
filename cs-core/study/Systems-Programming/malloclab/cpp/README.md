# Malloc Lab C++ 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 C 구현과 같은 `mm_*` 계약을 C++로 다시 구현합니다.
동일한 allocator 정책을 다른 언어 문법으로 유지하는 비교 경로입니다.

## 누구를 위한 문서인가

- C와 C++ allocator 구현을 비교하고 싶은 학습자
- 같은 API를 다른 언어 스타일로 정리하는 예시가 필요한 사람
- free list 정책을 언어별로 비교하고 싶은 사람

## 먼저 읽을 곳

1. [`../c/README.md`](../c/README.md)
2. [`../problem/README.md`](../problem/README.md)
3. `tests/`

## 디렉터리 구조

```text
cpp/
  README.md
  include/
    mm.h
    memlib.h
  src/
    mm.cpp
  tests/
  Makefile
```

## 검증 방법

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- README는 구현 범위와 검증 흐름만 설명합니다.
- allocator 세부 reasoning은 `docs/`에서 다룹니다.

## 포트폴리오로 확장하는 힌트

- 같은 allocator 정책을 두 언어에서 유지했다는 점을 한 줄로 명시해 두면 좋습니다.
