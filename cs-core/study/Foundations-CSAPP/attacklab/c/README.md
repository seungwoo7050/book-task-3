# Attack Lab C companion

## 이 디렉터리가 가르치는 것

이 디렉터리는 실제 exploit target을 재배포하지 않고도 payload 구조를 검증하는 C companion verifier를 제공합니다.
핵심은 바이트 나열이 어떤 공격 모델을 만족하는지 해석하는 것입니다.

## 누구를 위한 문서인가

- payload를 "실행"보다 "구조 검증" 관점에서 보고 싶은 학습자
- C로 phase별 검증 로직을 읽고 싶은 사람
- 공개 가능한 보안 과제 산출물 구조가 필요한 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../docs/README.md`](../docs/README.md)
3. [`tests/test_mini_attacklab.c`](tests/test_mini_attacklab.c)

## 디렉터리 구조

```text
c/
  README.md
  include/
    mini_attacklab.h
  src/
    mini_attacklab.c
    main.c
  tests/
    test_mini_attacklab.c
  data/
    phase1.txt
    phase2.txt
    phase3.txt
    phase4.txt
    phase5.txt
  Makefile
```

## 검증 방법

```bash
cd c
make clean && make test
```

## 스포일러 경계

- companion verifier는 payload 구조만 확인합니다.
- 외부 비공개 target에 직접 재사용 가능한 정보는 README에 늘리지 않습니다.

## 포트폴리오로 확장하는 힌트

- 보안 과제는 "왜 실행 대신 구조 검증 모델을 만들었는가"를 설명하면 공개 전략이 설득력 있어집니다.
