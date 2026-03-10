# Architecture Lab C companion

## 이 디렉터리가 가르치는 것

이 디렉터리는 Architecture Lab의 Part A/B/C 핵심 의미를 C 모델로 다시 실행하게 만듭니다.
공식 simulator가 없어도 명령어 의미, 제어 신호, 성능 비용 모델을 코드로 확인할 수 있습니다.

## 누구를 위한 문서인가

- Y86/HCL 실습 전에 의미 모델을 먼저 보고 싶은 학습자
- Part A/B/C를 C 코드로 비교하고 싶은 사람
- 공식 hand-in과 companion 모델을 구분해 관리하고 싶은 사람

## 먼저 읽을 곳

1. [`../problem/README.md`](../problem/README.md)
2. [`../y86/README.md`](../y86/README.md)
3. [`../docs/README.md`](../docs/README.md)

## 디렉터리 구조

```text
c/
  README.md
  include/
  src/
  tests/
  Makefile
```

## 검증 방법

```bash
cd c
make clean && make test
```

## 스포일러 경계

- 이 구현은 공식 simulator를 대체하는 답안이 아니라 개념 보조 모델입니다.
- README는 Part 대응 관계와 검증 경로만 설명합니다.

## 포트폴리오로 확장하는 힌트

- 아키텍처 프로젝트는 한 문제를 여러 추상화로 다시 모델링했다는 점을 강조하면 좋습니다.
