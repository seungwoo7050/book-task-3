# Attack Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 Attack Lab을 공개 문서로 설명할 때 필요한 payload 모델, ROP 사고법, 공개 정책을 정리합니다.
핵심은 공격 기법을 무책임하게 복제하는 것이 아니라, 왜 제약이 생기고 모델이 바뀌는지 이해하는 것입니다.

## 누구를 위한 문서인가

- 보안 실습 문서를 학습 가이드 형태로 남기고 싶은 학습자
- payload reasoning과 공개 정책을 함께 보고 싶은 사람
- companion verifier와 공식 문제 경계를 동시에 이해하고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/payload-models.md`](concepts/payload-models.md)
2. [`concepts/rop-and-relative-addressing.md`](concepts/rop-and-relative-addressing.md)
3. [`references/publication-policy.md`](references/publication-policy.md)
4. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    payload-models.md
    rop-and-relative-addressing.md
  references/
    publication-policy.md
    verification.md
```

## 검증 방법

- 실제 명령은 [`references/verification.md`](references/verification.md)에 정리되어 있습니다.
- 문서는 [`../problem/README.md`](../problem/README.md)의 복원 경로와 함께 읽는 것이 좋습니다.

## 스포일러 경계

- 공격 모델과 방어 차이는 설명합니다.
- 비공개 타깃에 바로 적용 가능한 raw exploit 정보는 늘리지 않습니다.

## 포트폴리오로 확장하는 힌트

- 보안 문서는 "공개 가능한 설명"과 "공개하지 않을 정보"를 함께 적을 때 신뢰도가 높습니다.
