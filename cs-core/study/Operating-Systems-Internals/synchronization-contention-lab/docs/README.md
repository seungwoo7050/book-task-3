# Synchronization Contention Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 synchronization primitive를 API 목록으로 나열하지 않고, 어떤 invariant를 지키기 위해 무엇을 쓰는지 설명한다. 특히 race-free correctness와 timing 측정을 어떻게 분리할지에 초점을 둔다.

## 누구를 위한 문서인가

- mutex, semaphore, condvar를 같은 과제처럼 비교해 보고 싶은 학습자
- contention benchmark에서 무엇을 테스트로 고정해야 하는지 알고 싶은 사람
- bounded buffer 같은 고전 예제를 실제 코드와 연결하고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/mutex-semaphore-condvar.md`](concepts/mutex-semaphore-condvar.md)
2. [`concepts/correctness-before-timing.md`](concepts/correctness-before-timing.md)
3. [`concepts/scenario-invariants.md`](concepts/scenario-invariants.md)
4. [`references/verification.md`](references/verification.md)
5. [`references/README.md`](references/README.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    mutex-semaphore-condvar.md
    correctness-before-timing.md
    scenario-invariants.md
  references/
    verification.md
    README.md
```

## 검증과 연결되는 파일

- metric shape와 field 의미는 [`../c/include/contention_lab.h`](../c/include/contention_lab.h)에 있다.
- 세 시나리오 구현은 [`../c/src/contention_lab.c`](../c/src/contention_lab.c)에 있다.
- invariant shell test는 [`../c/tests/test_cases.sh`](../c/tests/test_cases.sh)에 있다.
- 현재 검증 기준과 기대 신호는 [`references/verification.md`](references/verification.md)에 적어 둔다.

## 포트폴리오로 확장하는 힌트

- unsafe baseline을 같이 두면 synchronization이 “왜 필요한가”를 더 직접적으로 보여 줄 수 있다.
- thread sanitizer나 flamegraph를 붙이면 correctness와 performance debugging 두 축으로 확장할 수 있다.
