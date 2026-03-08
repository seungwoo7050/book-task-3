# 최소 스패닝 트리 (Kruskal) 개념 정리

## CLRS 연결
CLRS Ch 23.2 Kruskal's Algorithm — 간선을 가중치순 정렬 후 Union-Find로 사이클 체크.

## 알고리즘
1. 간선을 가중치 오름차순 정렬
2. 각 간선에 대해:
   - 두 끝점이 다른 집합 → Union, 간선 선택
   - 같은 집합 → 스킵 (사이클 방지)
3. $V-1$개 간선 선택 시 종료

## Union-Find 최적화
- **경로 압축**: `parent[x] = parent[parent[x]]` (Path Splitting)
- **랭크 합치기**: 작은 트리를 큰 트리에 합침
- 거의 $O(\alpha(N)) \approx O(1)$ 상각

## 복잡도
$O(E \log E)$ — 정렬이 병목.
