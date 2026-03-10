# Malloc Lab C 구현

## 이 디렉터리가 가르치는 것

이 디렉터리는 explicit free list allocator를 C로 구현합니다.
정렬, boundary tag, coalescing, in-place `realloc`을 실제 코드와 테스트로 확인하는 경로입니다.

## 누구를 위한 문서인가

- C로 allocator를 구현하고 싶은 학습자
- 불변식과 테스트를 함께 보고 싶은 사람
- trace 기반 검증 구조가 필요한 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../docs/README.md`](../docs/README.md)
3. `tests/`

## 디렉터리 구조

```text
c/
  README.md
  include/
    mm.h
    memlib.h
  src/
    mm.c
  tests/
  Makefile
```

## 검증 방법

```bash
cd c
make clean && make test
```

## 스포일러 경계

- README는 allocator 정책과 검증 경로만 설명합니다.
- 세부 블록 설계 reasoning은 `docs/`와 `notion/`으로 분리합니다.

## 포트폴리오로 확장하는 힌트

- allocator는 자료구조 선택 이유를 짧게 정리하는 것만으로도 강한 프로젝트가 됩니다.
