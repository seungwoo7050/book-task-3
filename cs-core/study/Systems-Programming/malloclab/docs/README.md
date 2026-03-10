# Malloc Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 allocator 불변식, coalescing 전략, `realloc` 검증 방식을 공개 문서로 정리합니다.
코드를 읽기 전에 어떤 규칙을 지켜야 하는지 확인하는 역할을 합니다.

## 누구를 위한 문서인가

- allocator 설계를 글로 먼저 정리하고 싶은 학습자
- free list 정책과 검증 기준을 문서화하고 싶은 사람
- 면접/복습용 개념 노트를 만들고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/allocator-invariants.md`](concepts/allocator-invariants.md)
2. [`concepts/realloc-and-coalescing.md`](concepts/realloc-and-coalescing.md)
3. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    allocator-invariants.md
    realloc-and-coalescing.md
  references/
    verification.md
```

## 검증 방법

- 검증 명령과 측정 결과는 [`references/verification.md`](references/verification.md)에 있습니다.
- 실제 구현 실행은 [`../c/README.md`](../c/README.md)와 [`../cpp/README.md`](../cpp/README.md)를 따릅니다.

## 스포일러 경계

- 공개 문서는 불변식과 전략을 설명합니다.
- 구현 코드 전체를 문서로 다시 싣지 않습니다.

## 포트폴리오로 확장하는 힌트

- allocator 프로젝트는 "내가 지킨 불변식 3개"만 잘 써도 매우 강해집니다.
