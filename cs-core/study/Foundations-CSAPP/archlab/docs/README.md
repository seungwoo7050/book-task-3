# Architecture Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 Architecture Lab이 왜 세 파트로 갈라지고, 각 파트가 무엇을 배우게 하는지 설명합니다.
공식 toolchain과 companion 모델의 역할을 한눈에 연결하는 것이 목적입니다.

## 누구를 위한 문서인가

- Part A/B/C의 관계를 먼저 이해하고 싶은 학습자
- 제어 신호와 pipeline cost를 글로 먼저 정리하고 싶은 사람
- 공개 가능한 설명과 로컬 복원 자산의 경계를 보고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/part-split.md`](concepts/part-split.md)
2. [`concepts/iaddq-and-control-signals.md`](concepts/iaddq-and-control-signals.md)
3. [`concepts/pipeline-cost-model.md`](concepts/pipeline-cost-model.md)
4. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    part-split.md
    iaddq-and-control-signals.md
    pipeline-cost-model.md
  references/
    verification.md
```

## 검증 방법

- 상세 명령은 [`references/verification.md`](references/verification.md)에 있습니다.
- 공식 검증 경로는 [`../problem/README.md`](../problem/README.md), hand-in 산출물은 [`../y86/README.md`](../y86/README.md)와 연결해 읽습니다.

## 스포일러 경계

- 공개 문서는 파트 구조와 reasoning을 설명합니다.
- 복원된 공식 toolchain 파일은 공개 트리에 넣지 않습니다.

## 포트폴리오로 확장하는 힌트

- 복잡한 프로젝트일수록 "한 문단 설명"보다 "파트별 연결도"가 더 읽기 쉽습니다.
