# 회고

> 프로젝트: 최소 스패닝 트리
> 아래 내용은 `notion-archive/03-retrospective.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 배운 것

크루스칼의 정당성: "가장 가벼운 간선이 사이클을 만들지 않으면, 어떤 MST에 포함된다" (컷 속성). Union-Find는 "두 노드가 같은 집합인가?"를 거의 $O(1)$에 판별하는 자료구조.

## 크루스칼 vs 프림

- 크루스칼: 간선 중심, 희소 그래프에 유리, $O(E \log E)$
- 프림: 정점 중심, 밀집 그래프에 유리, $O(E \log V)$

이 문제에서는 크루스칼이 구현이 더 간결.

## Union-Find의 재활용

Core-Bridges의 BOJ 1717이 Union-Find 전용 문제. 여기서 익힌 find/union을 그대로 쓸 수 있다.

## 이번 프로젝트가 남긴 기준

- `최소 스패닝 트리`를 통해 `그래프 전체 구조를 만들거나 순서를 고정하는 규칙을 설명하는 연습`를 코드와 문장으로 같이 설명하는 감각을 다시 확인했다.
- 짧은 정답 코드보다, 왜 이 선택이 안전했는지 적어 둔 문장이 나중에 더 오래 남는다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 다음 프로젝트로 가져갈 것

- 구현을 시작하기 전에 핵심 상태와 종료 조건을 먼저 적는다.
- 자동 검증이 통과한 뒤에야 문서 문장을 확정한다.
- 포트폴리오용 README로 옮길 때는 "선택 이유"와 "실수 포인트"를 먼저 보여 준다.
- `05-development-timeline.md`처럼 실행 순서와 검증 순서를 남기면, 시간이 지난 뒤에도 학습 과정을 다시 밟기 쉬워진다.

## 트랙 안에서 이어지는 연결

- 앞 프로젝트: [`../../2252/README.md`](../../2252/README.md) (줄 세우기)
- 현재 프로젝트를 다시 설명할 때는 같은 트랙의 앞뒤 프로젝트와 무엇이 달라졌는지 한 문장으로 비교해 두는 편이 좋다.

## 다시 확인할 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`kruskal-concept.md`](../docs/concepts/kruskal-concept.md)
