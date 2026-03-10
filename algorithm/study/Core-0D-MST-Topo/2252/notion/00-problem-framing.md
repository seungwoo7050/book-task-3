# 문제 프레이밍

> 프로젝트: 줄 세우기
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 22.4의 위상 정렬(Topological Sort). 부분 순서가 주어졌을 때 전체 순서를 결정하는 문제. BFS 기반(Kahn's Algorithm) 구현.

## 문제 구조

- $N$명 학생, $M$개 비교 (A가 B보다 앞)
- 조건을 만족하는 순서 하나 출력

## 왜 이 문제를 선택했는가

위상 정렬의 정석 문제. 진입 차수(in-degree) 기반 BFS가 가장 직관적.

## 난이도 평가

Gold. 알고리즘은 단순하지만, DAG 조건과 비유일 해를 이해해야 함.

## 지금 이 프로젝트에서 먼저 고정할 것

- `줄 세우기`에서 실제로 확인하려는 학습 목표는 `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`topological-sort-concept.md`](../docs/concepts/topological-sort-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../9372/README.md`](../../9372/README.md) (상근이의 여행)
