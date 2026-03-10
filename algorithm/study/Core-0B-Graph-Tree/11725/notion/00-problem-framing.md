# 문제 프레이밍

> 프로젝트: 트리의 부모 찾기
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

루트가 1인 트리에서 각 노드의 부모를 구하는 기초 문제. BFS로 루트부터 탐색하면 자연스럽게 부모가 결정된다.

## 문제 구조

- $N$개의 노드, $N-1$개의 간선
- 루트 = 1
- 2번부터 $N$번까지 각 노드의 부모 출력

## 왜 이 문제를 선택했는가

트리 BFS의 가장 기본적인 응용. "방문하지 않은 인접 노드 = 자식"이라는 트리의 성질을 익힌다.

## 난이도 평가

Bronze. BFS 기초.

## 지금 이 프로젝트에서 먼저 고정할 것

- `트리의 부모 찾기`에서 실제로 확인하려는 학습 목표는 `트리 구조의 성질을 이용해 탐색과 누적 계산을 재구성하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`tree-parent-concept.md`](../docs/concepts/tree-parent-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../1991/README.md`](../../1991/README.md) (트리 순회)
