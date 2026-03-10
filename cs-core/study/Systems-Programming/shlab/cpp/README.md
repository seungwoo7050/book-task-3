# Shell Lab C++ 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 C 구현과 같은 tiny shell 계약을 C++로 다시 구현합니다.
동일한 job control과 signal 규칙을 다른 언어 스타일로 유지하는 비교 경로입니다.

## 누구를 위한 문서인가

- C와 C++ 셸 구현을 비교하고 싶은 학습자
- C++로 signal-aware 테스트를 구성하는 예시가 필요한 사람
- 다중 구현 저장소 구조를 참고하고 싶은 사람

## 먼저 읽을 곳

1. [`../c/README.md`](../c/README.md)
2. [`../problem/README.md`](../problem/README.md)
3. `tests/run_tests.sh`

## 디렉터리 구조

```text
cpp/
  README.md
  include/
    tsh_helper.hpp
  src/
    tsh.cpp
  tests/
    run_tests.sh
    traces/
  Makefile
```

## 검증 방법

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- README는 구현 범위와 검증 흐름만 설명합니다.
- 시그널 race 해설은 `docs/`에서 다룹니다.

## 포트폴리오로 확장하는 힌트

- 동일 계약의 언어별 구현 차이를 짧게 비교해 적으면 좋습니다.
