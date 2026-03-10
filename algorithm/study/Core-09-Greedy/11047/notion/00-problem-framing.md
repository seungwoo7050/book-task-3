# 문제 프레이밍

> 프로젝트: 동전 0
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 16 그리디 알고리즘의 입문 문제. $N$종류의 동전으로 금액 $K$를 만들 때, 최소 동전 개수를 구한다. 동전이 오름차순이고 "각 동전이 이전 동전의 배수"라는 조건 덕분에 그리디가 최적해를 보장한다.

## 문제 구조

- $N$개 동전 (오름차순, 각각이 이전의 배수)
- 금액 $K$
- 최소 동전 개수 출력

## 왜 이 문제를 선택했는가

그리디의 가장 기초적인 형태. "큰 것부터 쓰면 최적"이라는 직관이 왜 이 경우에 정당한지, 그리고 배수 조건이 없으면 왜 깨지는지를 이해하는 출발점이다.

## 난이도 평가

Bronze. 점화식 필요 없이, 큰 동전부터 나누기/나머지 연산만 하면 된다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `동전 0`에서 실제로 확인하려는 학습 목표는 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`greedy-coin-concept.md`](../docs/concepts/greedy-coin-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../1931/README.md`](../../1931/README.md) (회의실 배정)
