# Bomb Lab C++ companion

## 이 디렉터리가 가르치는 것

이 디렉터리는 C companion과 같은 phase 계약을 C++로 다시 구현해, 언어가 달라도 학습 경계는 유지할 수 있음을 보여 줍니다.
파싱과 검증을 C++ 표준 라이브러리로 옮긴 비교 기준점입니다.

## 누구를 위한 문서인가

- C와 C++ companion 구현을 나란히 보고 싶은 학습자
- phase 검증 로직을 C++ 스타일로 보고 싶은 사람
- 다중 언어 구현을 같은 문제 경계 안에 넣는 예시가 필요한 사람

## 먼저 읽을 곳

1. [`../c/README.md`](../c/README.md)
2. [`../problem/README.md`](../problem/README.md)
3. [`tests/test_mini_bomb.cpp`](tests/test_mini_bomb.cpp)

## 디렉터리 구조

```text
cpp/
  README.md
  include/
    mini_bomb.hpp
  src/
    mini_bomb.cpp
    main.cpp
  tests/
    test_mini_bomb.cpp
  Makefile
```

## 검증 방법

```bash
cd cpp
make clean && make test

printf 'Assembly reveals intent.\n1 2 4 8 16 32\n1 311\n6 6\n01234.\n4 6 2 3 5 1\n35\n' > /tmp/bomblab_cpp_answers.txt
./build/mini_bomb /tmp/bomblab_cpp_answers.txt
rm /tmp/bomblab_cpp_answers.txt
```

## 스포일러 경계

- C++ 구현도 공식 bomb 자체를 대체한다고 주장하지 않습니다.
- README는 phase 계약과 검증 흐름만 다루고, 외부 타깃 정보는 싣지 않습니다.

## 포트폴리오로 확장하는 힌트

- 동일 계약을 다른 언어로 옮길 때 어떤 설계 요소가 유지되는지 비교해 적으면 좋습니다.
