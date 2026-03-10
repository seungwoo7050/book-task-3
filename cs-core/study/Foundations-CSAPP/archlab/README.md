# Architecture Lab

## 이 프로젝트가 가르치는 것

`archlab`은 Y86-64 어셈블리, HCL 제어 로직, 파이프라인 성능 최적화를 한 프로젝트 안에서 연결해 보여 줍니다.
같은 과제 안에서 "명령어를 쓰는 법", "명령어를 구현하는 법", "명령어를 빠르게 돌리는 법"이 어떻게 이어지는지 배우게 합니다.

## 누구를 위한 문서인가

- 아키텍처 실습이 여러 파트로 나뉘어 있어 전체 그림을 먼저 보고 싶은 학습자
- 공식 hand-in 파일과 companion 모델의 관계를 이해하고 싶은 사람
- 공개 가능한 산출물과 로컬 복원 툴체인을 함께 관리하고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`y86/README.md`](y86/README.md)
3. [`c/README.md`](c/README.md)
4. [`cpp/README.md`](cpp/README.md)
5. [`docs/README.md`](docs/README.md)
6. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
archlab/
  README.md
  problem/
  y86/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

공식 self-study handout 검증:

```bash
cd problem
make restore-official
make verify-official
```

C companion 검증:

```bash
cd c
make clean && make test
```

C++ companion 검증:

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- 공개 문서는 파트 분해, 제어 신호 사고법, 성능 모델을 설명합니다.
- 공식 simulator/HCL toolchain은 `problem/official/` 아래 로컬에서만 복원합니다.
- README는 학습 구조를 설명하고, 세부 구현 근거는 `docs/`와 `notion/`으로 분리합니다.

## 포트폴리오로 확장하는 힌트

- 이 프로젝트는 "한 문제를 여러 추상화 계층에서 다뤘다"는 점을 보여 주기 좋습니다.
- 개인 저장소에서는 Part A/B/C를 각기 다른 산출물로 나누어 캡처와 성능 비교를 붙이면 훨씬 읽기 쉬워집니다.
