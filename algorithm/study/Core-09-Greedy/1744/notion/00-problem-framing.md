# 문제 프레이밍

> 프로젝트: 수 묶기
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

$N$개의 정수를 2개씩 묶거나 묶지 않아서 합을 최대화하는 문제. 곱은 양수×양수를 크게 만들고, 음수×음수를 양수로 바꾸는 데 유리하다. 하지만 1은 묶으면 손해(1×x < 1+x), 0은 음수를 상쇄하는 데 쓸 수 있다.

## 문제 구조

- $N$개의 정수 (음수, 0, 양수 혼재)
- 2개씩 묶으면 곱을 합에 기여, 안 묶으면 값 자체를 기여
- 최대 합 출력

## 왜 이 문제를 선택했는가

단순 그리디(동전 0)보다 케이스 분류가 복잡한 Gold 그리디. 양수/음수/0/1을 어떻게 분류하고 짝지을 것인가를 사고하는 훈련.

## 난이도 평가

Gold. 분류 실수가 잦아 디버깅 난이도가 높다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `수 묶기`에서 실제로 확인하려는 학습 목표는 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`bundling-greedy-concept.md`](../docs/concepts/bundling-greedy-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1931/README.md`](../../1931/README.md) (회의실 배정)
