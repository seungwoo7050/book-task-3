# Architecture Lab C++ companion

## 이 디렉터리가 가르치는 것

이 디렉터리는 C companion과 같은 Part A/B/C 대응을 C++로 다시 구현합니다.
값 타입과 표준 컨테이너를 써도 문제 계약을 어떻게 유지하는지 보여 줍니다.

## 누구를 위한 문서인가

- C와 C++ companion 모델을 비교하고 싶은 학습자
- C++로 아키텍처 개념 모델을 정리하는 예시가 필요한 사람
- 동일 계약의 다중 구현 구조를 참고하고 싶은 사람

## 먼저 읽을 곳

1. [`../c/README.md`](../c/README.md)
2. [`../y86/README.md`](../y86/README.md)
3. [`../docs/README.md`](../docs/README.md)

## 디렉터리 구조

```text
cpp/
  README.md
  include/
  src/
  tests/
  Makefile
```

## 검증 방법

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- README는 companion 모델의 역할과 검증 흐름만 설명합니다.
- 공식 simulator 내부 파일은 로컬 복원 경로로만 다룹니다.

## 포트폴리오로 확장하는 힌트

- 다중 언어 비교 시 어떤 추상화가 공통으로 유지되는지 짚어 주면 좋습니다.
