# Data Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 bit puzzle을 푸는 반복 패턴, 부동소수점 경계값, 검증 흐름을 공개 문서로 정리합니다.
코드 전체를 복붙하는 대신 왜 그런 패턴이 통하는지 설명하는 역할을 맡습니다.

## 누구를 위한 문서인가

- 구현 전에 핵심 사고법을 먼저 훑고 싶은 학습자
- 설명 문서와 실제 코드의 역할을 분리하고 싶은 사람
- README보다 조금 더 깊은 개념 정리가 필요한 사람

## 먼저 읽을 곳

1. [`concepts/integer-patterns.md`](concepts/integer-patterns.md)
2. [`concepts/float-boundaries.md`](concepts/float-boundaries.md)
3. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    integer-patterns.md
    float-boundaries.md
  references/
    verification.md
```

## 검증 방법

- 구현 검증 명령은 [`../README.md`](../README.md)와 [`references/verification.md`](references/verification.md)에 정리되어 있습니다.
- 개념 문서는 실제 구현 및 테스트 경로와 함께 읽을 때 가장 효과적입니다.

## 스포일러 경계

- 공개 문서는 풀이 원리와 경계값 사고를 설명합니다.
- 최종 구현 전체를 문서로 다시 싣지는 않습니다.

## 포트폴리오로 확장하는 힌트

- `docs/`는 "내가 배운 개념"을 짧고 재사용 가능하게 남기는 곳으로 쓰면 좋습니다.
