# 문제 프레이밍

> 프로젝트: N-Queen
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

$N \times N$ 체스판에 $N$개의 퀸을 서로 공격하지 않게 배치하는 경우의 수를 구하는 고전적인 문제. 백트래킹의 교과서적 예시로, 15649의 "선택 → 재귀 → 되돌림" 패턴에 **가지치기(pruning)**가 추가된다.

## 문제 구조 파악

- $1 \leq N \leq 15$
- 퀸은 같은 행, 열, 대각선에 있으면 서로 공격
- 유효한 배치의 총 수 출력

행 단위로 퀸을 배치하면, 각 행에 정확히 하나만 놓으므로 $N$개의 "열 선택"만 결정하면 된다. 하지만 열 충돌과 대각선 충돌을 체크해야 한다.

## 왜 이 문제를 선택했는가

Core-04의 Gold 문제로, 백트래킹의 핵심인 "유망성 판단"의 효율적 구현을 훈련한다. 15649에서는 가지치기가 사실상 없었지만, N-Queen에서는 열과 대각선 검사로 탐색 공간을 극적으로 줄인다.

## 난이도 평가

Gold 등급. $N = 15$에서 순수 완전 탐색은 $15!$이지만, 가지치기로 실제 탐색량은 훨씬 적다. Python으로는 시간이 빡빡해 C++ 구현도 유지한다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `N-Queen`에서 실제로 확인하려는 학습 목표는 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`nqueen-concept.md`](../docs/concepts/nqueen-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../15649/README.md`](../../15649/README.md) (N과 M (1))
