# Shell Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 job control, process group, signal race를 공개 문서로 설명합니다.
코드만 읽어서는 잘 보이지 않는 동작 순서를 정리하는 역할을 합니다.

## 누구를 위한 문서인가

- 셸 구현 전에 개념 흐름을 먼저 정리하고 싶은 학습자
- 시그널 race를 글과 그림으로 설명하고 싶은 사람
- 테스트 정책을 문서화하고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/signal-and-race-discipline.md`](concepts/signal-and-race-discipline.md)
2. [`concepts/job-control-flow.md`](concepts/job-control-flow.md)
3. [`references/verification.md`](references/verification.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    signal-and-race-discipline.md
    job-control-flow.md
  references/
    verification.md
```

## 검증 방법

- 검증 명령과 trace 범위는 [`references/verification.md`](references/verification.md)에 정리되어 있습니다.
- 실제 실행은 [`../c/README.md`](../c/README.md) 또는 [`../cpp/README.md`](../cpp/README.md)를 따릅니다.

## 스포일러 경계

- 공개 문서는 race와 job control 원리를 설명합니다.
- starter asset 자체는 공개하지 않습니다.

## 포트폴리오로 확장하는 힌트

- 동시성/시그널 문서는 타임라인 그림이나 상태 전이를 함께 두면 훨씬 읽기 좋습니다.
