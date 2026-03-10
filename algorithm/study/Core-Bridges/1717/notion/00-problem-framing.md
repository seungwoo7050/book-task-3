# 문제 프레이밍

> 프로젝트: 집합의 표현
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 21 Disjoint Set Union의 직접 구현 문제. 합집합(Union)과 같은 집합 판별(Find) 연산만 수행하는 순수한 자료구조 문제.

## 문제 구조

- $N+1$개 원소 (0부터 N)
- $M$개 연산: 합치기(0) 또는 같은 집합인지 확인(1)
- 확인 연산마다 YES/NO 출력

## 왜 이 문제를 선택했는가

Core-Bridges 프로젝트. 크루스칼(BOJ 1197)에서 사용한 Union-Find를 독립적으로 훈련하기 위한 브릿지.

## 난이도 평가

Gold. Union-Find 최적화(경로 압축)가 없으면 TLE.

## 지금 이 프로젝트에서 먼저 고정할 것

- `집합의 표현`에서 실제로 확인하려는 학습 목표는 `다음 트랙에서 필요한 선행 개념을 별도 실습으로 고정하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 다음 트랙에서 다시 만나게 될 선행 개념을 지금 확실히 고정해 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`disjoint-set-union.md`](../docs/concepts/disjoint-set-union.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 같은 트랙의 큰 흐름은 [`../../README.md`](../../README.md)에서 다시 확인한다.
