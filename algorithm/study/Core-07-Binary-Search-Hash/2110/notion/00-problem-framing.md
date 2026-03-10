# 문제 프레이밍

> 프로젝트: 공유기 설치
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

"최솟값의 최댓값을 구하라"는 요구는 **매개변수 탐색(parametric search)**의 전형적인 신호다. 답이 될 수 있는 값의 범위에서 이진 탐색을 하고, "이 값이 가능한가?"를 판별 함수로 확인한다.

## 문제 구조

- 수직선 위 $N$개의 집 ($N \leq 200,000$)
- $C$개의 공유기를 설치, 어떤 두 공유기 사이의 최소 거리를 최대화
- 좌표 범위 $\leq 10^9$

## 왜 이 문제를 선택했는가

Core-07의 Gold 문제로, 이진 탐색을 "배열에서 값 찾기"가 아닌 **"답의 범위에서 최적값 찾기"**로 확장한다. 이 패턴은 최적화 문제에서 매우 자주 등장한다.

## 난이도 평가

Gold 등급. "답에 대해 이진 탐색한다"는 아이디어를 떠올리는 것이 핵심. 판별 함수(`feasible`)를 설계하면 구현은 직관적.

## 지금 이 프로젝트에서 먼저 고정할 것

- `공유기 설치`에서 실제로 확인하려는 학습 목표는 `탐색 대상을 재정의하고 자료구조 또는 매개변수 탐색으로 문제를 다시 보는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`parametric-search-concept.md`](../docs/concepts/parametric-search-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../10816/README.md`](../../10816/README.md) (숫자 카드 2)
