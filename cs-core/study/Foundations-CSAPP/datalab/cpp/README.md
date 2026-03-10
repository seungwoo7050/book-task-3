# Data Lab C++ 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 같은 문제 계약을 C++로 다시 풀면서 언어 문법이 달라도 관찰 가능한 동작은 같아야 한다는 점을 보여 줍니다.
주요 목적은 C 구현과 나란히 비교 가능한 기준점을 만드는 것입니다.

## 누구를 위한 문서인가

- C와 C++로 같은 bit puzzle을 비교하고 싶은 학습자
- C++ 테스트만 빠르게 실행해 보고 싶은 사람
- 동일 계약의 다중 구현을 저장소에 배치하는 예시가 필요한 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../c/README.md`](../c/README.md)
3. [`tests/test_bits.cpp`](tests/test_bits.cpp)

## 디렉터리 구조

```text
cpp/
  README.md
  src/
    bits.cpp
  tests/
    test_bits.cpp
```

## 검증 방법

```bash
cd cpp/tests
g++ -std=c++20 -O1 -Wall -Werror -o test_bits_cpp test_bits.cpp ../src/bits.cpp
./test_bits_cpp
```

## 스포일러 경계

- README는 구현 비교 관점과 테스트 경로만 설명합니다.
- 세부 풀이 패턴은 `docs/`와 `notion/`에서 다룹니다.

## 포트폴리오로 확장하는 힌트

- 같은 문제를 두 언어로 맞춘 이유를 짧게 적으면 설계 의도가 분명해집니다.
