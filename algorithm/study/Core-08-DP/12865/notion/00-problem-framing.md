# 문제 프레이밍

> 프로젝트: 평범한 배낭
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 15의 대표 문제인 0/1 배낭 문제. $N$개의 물건 중 무게 합이 $K$를 넘지 않으면서 가치 합을 최대화한다. DP의 "최적 부분구조"와 "중복 부분문제"를 가장 잘 보여주는 고전.

## 문제 구조

- $N$개의 물건 ($N \leq 100$), 각각 무게 $W_i$와 가치 $V_i$
- 배낭 용량 $K$ ($K \leq 100,000$)
- 각 물건은 최대 1개 선택 가능
- 최대 가치 합 출력

## 왜 이 문제를 선택했는가

Core-08의 Gold 문제로, 2차원 DP를 1차원으로 최적화하는 기법을 훈련한다. DP 테이블의 의미를 정확히 이해해야 역순 순회의 정당성을 납득할 수 있다.

## 난이도 평가

Gold 등급. 점화식은 교과서적이지만, 1D 배열 역순 순회의 이유를 이해하는 것이 핵심.

## 지금 이 프로젝트에서 먼저 고정할 것

- `평범한 배낭`에서 실제로 확인하려는 학습 목표는 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`knapsack-concept.md`](../docs/concepts/knapsack-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1149/README.md`](../../1149/README.md) (RGB거리)
