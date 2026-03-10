# Performance Lab

## 이 프로젝트가 가르치는 것

`perflab`은 캐시 시뮬레이터와 행렬 전치 최적화를 통해 "정답이 맞는가"를 넘어 "왜 더 빠른가"를 설명하게 만드는 프로젝트입니다.
주소 분해, LRU 교체, locality, miss count 중심의 성능 측정이 핵심 학습 포인트입니다.

## 누구를 위한 문서인가

- 캐시 동작을 추상 설명이 아니라 실행 가능한 코드로 이해하고 싶은 학습자
- 성능 과제를 wall-clock time 대신 재현 가능한 지표로 정리하고 싶은 사람
- 동일 계약을 C와 C++로 비교해 보고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`c/README.md`](c/README.md)
3. [`cpp/README.md`](cpp/README.md)
4. [`docs/README.md`](docs/README.md)
5. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
perflab/
  README.md
  problem/
  c/
  cpp/
  docs/
  notion/
  notion-archive/
```

## 검증 방법

2026-03-10 문서 정비 기준으로 유지하는 검증 경로는 다음과 같습니다.

문제 경계 확인:

```bash
cd problem
make status
make compile
```

C 구현 검증:

```bash
cd c
make clean && make test
```

C++ 구현 검증:

```bash
cd cpp
make clean && make test
```

## 스포일러 경계

- 공개 문서는 캐시 모델과 최적화 전략을 설명합니다.
- 특정 코드 블록 전체를 해답처럼 붙여 넣기보다, miss를 줄이는 원리를 중심으로 정리합니다.
- `problem/`은 self-written starter boundary만 유지합니다.

## 포트폴리오로 확장하는 힌트

- 성능 과제는 "무엇을 측정했고 왜 그 지표를 믿는가"를 쓰는 것이 중요합니다.
- 개인 저장소에서는 naive 버전과 최적화 버전의 miss 차이를 표로 추가하면 훨씬 설득력이 생깁니다.
