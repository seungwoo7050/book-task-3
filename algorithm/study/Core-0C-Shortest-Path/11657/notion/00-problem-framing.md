# 문제 프레이밍

> 프로젝트: 타임머신
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

음의 가중치가 있는 방향 그래프에서 단일 출발점 최단 경로. 다익스트라가 못 하는 영역. 벨만-포드 알고리즘으로 음의 사이클도 탐지해야 한다.

## 문제 구조

- $N$개 도시, $M$개 버스 (방향, 음수 비용 가능)
- 1번에서 나머지까지 최단 시간
- 음의 사이클 존재 시 `-1` 출력

## 왜 이 문제를 선택했는가

Core-0C의 Gold 문제. 벨만-포드의 정당성(V-1번 반복)과 음의 사이클 탐지(V번째 반복에서 갱신)를 실전으로 익힌다.

## 난이도 평가

Gold. 간선 리스트 순회 + 음의 사이클 판정.

## 지금 이 프로젝트에서 먼저 고정할 것

- `타임머신`에서 실제로 확인하려는 학습 목표는 `가중치 조건과 그래프 특성에 맞는 최단 경로 알고리즘을 선택하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`bellman-ford-concept.md`](../docs/concepts/bellman-ford-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1753/README.md`](../../1753/README.md) (최단경로)
