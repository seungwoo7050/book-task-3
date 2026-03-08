# Disjoint Set Union

서로소 집합 자료구조는 원소가 어떤 그룹에 속하는지 빠르게 판단하고, 두 그룹을 합치는 연산을 지원한다.

- `find(x)`: 대표 원소를 찾는다.
- `union(a, b)`: 두 집합을 하나로 합친다.
- path compression과 union heuristic을 같이 쓰면 거의 상수 시간에 가깝게 동작한다.

이 개념은 Kruskal MST, 친구 관계 묶기, 연결성 질의 문제의 기초가 된다.
