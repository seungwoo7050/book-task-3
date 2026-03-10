# BOJ 1197 — 접근 과정

## 크루스칼 알고리즘

1. 모든 간선을 가중치 기준 정렬
2. 가장 가벼운 간선부터 순회
3. 두 끝점이 같은 집합이 아니면 선택 (Union)
4. $V-1$개 간선을 선택하면 종료

```python
edges.sort()  # (weight, a, b)
for w, a, b in edges:
    if union(parent, rank, a, b):
        total += w
        cnt += 1
        if cnt == v - 1:
            break
```

## Union-Find 최적화

- **경로 압축**: `parent[x] = parent[parent[x]]` (path splitting)
- **유니온 바이 랭크**: 작은 트리를 큰 트리 아래에 붙임

```python
def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path splitting
        x = parent[x]
    return x
```

## 시간/공간

- $O(E \log E)$ 정렬 + $O(E \cdot \alpha(V))$ Union-Find ≈ $O(E \log E)$
