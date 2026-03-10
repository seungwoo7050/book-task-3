# Performance Lab C++ 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 C 구현과 같은 cache simulator/transpose 계약을 C++로 다시 구현합니다.
같은 성능 과제를 다른 언어 스타일로 비교하는 기준점입니다.

## 누구를 위한 문서인가

- C와 C++ 구현의 차이를 비교하고 싶은 학습자
- C++ 표준 라이브러리 기반 성능 과제 구조를 보고 싶은 사람
- 동일 계약의 이중 구현을 정리하고 싶은 사람

## 먼저 읽을 곳

1. [`../c/README.md`](../c/README.md)
2. [`../problem/README.md`](../problem/README.md)
3. `tests/test_perflab.cpp`

## 디렉터리 구조

```text
cpp/
  README.md
  include/
    perflab.hpp
  src/
  tests/
    test_perflab.cpp
  Makefile
```

## 검증 방법

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- README는 구현 범위와 검증 경로만 설명합니다.
- 최적화 세부 reasoning은 `docs/`에서 다룹니다.

## 포트폴리오로 확장하는 힌트

- 같은 miss 기준을 두 언어에서 유지했다는 점을 짧게 적으면 설계 선택이 분명해집니다.
