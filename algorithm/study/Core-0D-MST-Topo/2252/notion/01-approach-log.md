# BOJ 2252 — 접근 과정

## Kahn's Algorithm (BFS 위상 정렬)

1. 진입 차수가 0인 노드를 큐에 삽입
2. 큐에서 꺼내 결과에 추가
3. 해당 노드의 간선을 제거 (인접 노드의 진입 차수 감소)
4. 진입 차수가 0이 된 노드를 큐에 추가
5. 큐가 빌 때까지 반복

```python
q = deque()
for i in range(1, n + 1):
    if indeg[i] == 0:
        q.append(i)
result = []
while q:
    u = q.popleft()
    result.append(str(u))
    for v in adj[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
```

## 정당성

DAG에서 항상 진입 차수 0인 노드가 존재. 그것을 제거하면 나머지도 DAG. 귀납적으로 전체 순서 결정.

## 시간/공간

- $O(V + E)$
