# Attack Lab C++ companion

## 이 디렉터리가 가르치는 것

이 디렉터리는 C companion과 같은 payload 계약을 C++로 다시 구현합니다.
바이트 파싱과 phase 검증을 C++ 스타일로 정리한 비교 기준점입니다.

## 누구를 위한 문서인가

- 같은 공격 모델을 C와 C++로 비교하고 싶은 학습자
- C++ 표준 라이브러리 기반 파서 구성이 궁금한 사람
- 다중 구현 비교형 저장소를 설계하고 싶은 사람

## 먼저 읽을 곳

1. [`../c/README.md`](../c/README.md)
2. [`../problem/README.md`](../problem/README.md)
3. [`tests/test_mini_attacklab.cpp`](tests/test_mini_attacklab.cpp)

## 디렉터리 구조

```text
cpp/
  README.md
  include/
    mini_attacklab.hpp
  src/
    mini_attacklab.cpp
    main.cpp
  tests/
    test_mini_attacklab.cpp
  data/
    phase1.txt
    phase2.txt
    phase3.txt
    phase4.txt
    phase5.txt
  Makefile
```

## 검증 방법

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- C++ 구현도 공개 가능한 companion 검증기로만 다룹니다.
- 외부 target raw exploit 정보는 README에 싣지 않습니다.

## 포트폴리오로 확장하는 힌트

- 동일 계약의 다중 구현을 비교한 이유를 쓰면 저장소 설계 의도가 명확해집니다.
