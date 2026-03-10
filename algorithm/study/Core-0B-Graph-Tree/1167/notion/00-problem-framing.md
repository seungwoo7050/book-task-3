# 문제 프레이밍

> 프로젝트: 트리의 지름
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

트리에서 가장 먼 두 점 사이의 거리(지름)를 구하는 문제. 가중치가 있는 트리에서 "임의의 점에서 가장 먼 점을 찾고, 그 점에서 다시 가장 먼 점을 찾으면 지름"이라는 정리를 활용한다.

## 문제 구조

- $V$개의 정점, 가중치 있는 트리
- 각 정점의 인접 리스트가 주어짐 (끝은 -1)
- 트리의 지름(최장 경로의 길이) 출력

## 왜 이 문제를 선택했는가

Core-0B의 Gold 문제로, 트리의 성질(유일한 경로)과 BFS 활용을 동시에 훈련한다. "두 번의 BFS"라는 우아한 알고리즘의 정당성 증명이 중요.

## 난이도 평가

Gold. 입력 파싱이 까다롭고, 두 번 BFS의 정당성 이해가 필요.

## 지금 이 프로젝트에서 먼저 고정할 것

- `트리의 지름`에서 실제로 확인하려는 학습 목표는 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`tree-diameter-concept.md`](../docs/concepts/tree-diameter-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1991/README.md`](../../1991/README.md) (트리 순회)
