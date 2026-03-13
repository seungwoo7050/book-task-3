# BOJ 1197 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 가중치 무방향 그래프에서 최소 스패닝 트리(MST)의 가중치 합을 구한다.
- 진행: Kruskal과 Prim 중에 고민했다. 간선 정렬 + 유니온파인드로 구현하는 Kruskal이 더 직관적이었다.
- 이슈: 유니온파인드를 제대로 구현해야 한다. path compression과 union by rank를 둘 다 쓰면 거의 O(α(N))이다.
- 판단: 간선을 가중치 순 정렬 → 사이클이 안 생기면(같은 집합이 아니면) 선택 → V-1개 간선을 고르면 종료.

### Session 2
- 목표: Kruskal을 구현한다.

이 시점의 핵심 코드:

```python
def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path compression
        x = parent[x]
    return x

def union(parent, rank, a, b):
    a, b = find(parent, a), find(parent, b)
    if a == b:
        return False
    if rank[a] < rank[b]:
        a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]:
        rank[a] += 1
    return True
```

path compression을 재귀 대신 "할아버지 포인터(parent[x] = parent[parent[x]])"로 구현한 게 반복적 방식이다. 처음엔 재귀로 했는데 Python 재귀 제한이 걱정되어 바꿨다.

CLI:

```bash
$ make -C study/Core-0D-MST-Topo/1197/problem run-py
```

```text
3
```

- 다음: 간선 수가 V-1개에 못 미치는 경우(비연결 그래프)는 이 문제에서 없는지 확인한다.
