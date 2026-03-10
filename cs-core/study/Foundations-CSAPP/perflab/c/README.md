# Performance Lab C 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 cache simulator와 transpose 최적화를 C로 구현하고 검증합니다.
기능 정합성과 miss 중심 성능 측정을 함께 다루는 구현 경로입니다.

## 누구를 위한 문서인가

- C로 cache simulator를 직접 작성하고 싶은 학습자
- transpose 최적화와 검증 하네스를 함께 보고 싶은 사람
- 성능 과제를 재현 가능한 테스트로 묶고 싶은 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../docs/README.md`](../docs/README.md)
3. `tests/test_perflab.c`

## 디렉터리 구조

```text
c/
  README.md
  include/
    perflab.h
  src/
  tests/
    test_perflab.c
  Makefile
```

## 검증 방법

```bash
cd c
make clean && make test
```

## 스포일러 경계

- README는 구현 범위와 검증 명령만 설명합니다.
- 구체 최적화 기법은 `docs/`에서 다룹니다.

## 포트폴리오로 확장하는 힌트

- 성능 측정 기준과 oracle 비교 기준을 함께 적으면 결과 신뢰도가 높아집니다.
