# Bomb Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 Bomb Lab을 공개 저장소에서 설명할 때 필요한 최소한의 워크플로, phase 패턴, 공개 범위를 정리합니다.
핵심은 해답집이 아니라 학습 가이드로 남기는 것입니다.

## 누구를 위한 문서인가

- 역공학 과제를 문서로 정리하는 방식이 필요한 학습자
- 공개 가능한 설명과 비공개로 남겨야 할 정보를 구분하고 싶은 사람
- companion 구현과 공식 문제를 함께 읽고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/reverse-engineering-workflow.md`](concepts/reverse-engineering-workflow.md)
2. [`concepts/phase-patterns.md`](concepts/phase-patterns.md)
3. [`references/publication-policy.md`](references/publication-policy.md)
4. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    reverse-engineering-workflow.md
    phase-patterns.md
  references/
    publication-policy.md
    verification.md
```

## 검증 방법

- 실제 명령은 [`references/verification.md`](references/verification.md)에 정리되어 있습니다.
- 문서를 읽은 뒤 [`../problem/README.md`](../problem/README.md)의 복원 경로와 함께 보는 것이 좋습니다.

## 스포일러 경계

- phase 패턴과 워크플로는 설명합니다.
- 특정 비공개 bomb의 raw answer와 대량 disassembly dump는 싣지 않습니다.

## 포트폴리오로 확장하는 힌트

- 역공학 문서는 "도구 사용 순서"를 체크리스트로 정리하면 읽는 사람이 훨씬 빨리 이해합니다.
