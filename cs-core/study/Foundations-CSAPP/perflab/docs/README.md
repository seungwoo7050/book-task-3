# Performance Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 cache simulator와 transpose 최적화를 문서로 설명합니다.
핵심은 성능을 재현 가능한 miss 기준으로 설명하는 것입니다.

## 누구를 위한 문서인가

- 구현 전에 locality와 LRU 개념을 먼저 정리하고 싶은 학습자
- benchmark policy를 문서로 남기고 싶은 사람
- 성능 과제 문서를 해설서 대신 가이드로 쓰고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/cache-sim-lru.md`](concepts/cache-sim-lru.md)
2. [`concepts/transpose-strategies.md`](concepts/transpose-strategies.md)
3. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    cache-sim-lru.md
    transpose-strategies.md
  references/
    verification.md
```

## 검증 방법

- 상세 명령과 기준값은 [`references/verification.md`](references/verification.md)에 정리되어 있습니다.
- 구현 검증은 [`../c/README.md`](../c/README.md), [`../cpp/README.md`](../cpp/README.md)와 함께 읽습니다.

## 스포일러 경계

- 공개 문서는 miss를 줄이는 원리와 검증 기준을 설명합니다.
- 특정 최적화 코드를 통째로 답안처럼 다시 싣지는 않습니다.

## 포트폴리오로 확장하는 힌트

- 성능 문서는 "무엇을 측정했고 왜 그 측정이 타당한가"를 명확히 적는 것이 핵심입니다.
