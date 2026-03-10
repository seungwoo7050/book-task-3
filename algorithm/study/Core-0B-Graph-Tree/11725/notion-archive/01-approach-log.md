# BOJ 11725 — 접근 과정

## 핵심

루트(1)에서 BFS. 처음 방문하는 순간, 탐색 출발점이 부모.

```python
visited[1] = True
q = deque([1])
while q:
    u = q.popleft()
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True
            parent[v] = u
            q.append(v)
```

## 출력

2번부터 $N$번까지 순서대로 `parent[i]` 출력.

## 시간/공간

- $O(N)$
