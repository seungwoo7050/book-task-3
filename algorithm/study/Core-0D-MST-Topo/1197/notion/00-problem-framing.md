# 문제 프레이밍

> 프로젝트: 최소 스패닝 트리
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 23의 대표 문제. 무방향 가중 그래프의 MST 가중치 합. 크루스칼 알고리즘 + Union-Find로 구현.

## 문제 구조

- $V$개 정점, $E$개 간선 (무방향, 가중)
- MST의 총 가중치 출력

## 왜 이 문제를 선택했는가

MST 알고리즘의 정석. 크루스칼(간선 정렬 + Union-Find)과 프림(힙 기반) 중 크루스칼을 선택한 이유와 Union-Find의 최적화(경로 압축 + 랭크)를 배운다.

## 난이도 평가

Silver. 크루스칼 자체는 단순하지만, Union-Find 구현이 핵심.

## 지금 이 프로젝트에서 먼저 고정할 것

- `최소 스패닝 트리`에서 실제로 확인하려는 학습 목표는 `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`kruskal-concept.md`](../docs/concepts/kruskal-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../2252/README.md`](../../2252/README.md) (줄 세우기)
