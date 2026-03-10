# BOJ 1916 — 접근 과정

## 핵심

1753과 동일한 다익스트라. 차이: 마지막에 `dist[e]`만 출력.

```python
dist = [INF] * (n + 1)
dist[s] = 0
hq = [(0, s)]
while hq:
    d, u = heapq.heappop(hq)
    if d > dist[u]:
        continue
    for v, w in adj[u]:
        nd = d + w
        if nd < dist[v]:
            dist[v] = nd
            heapq.heappush(hq, (nd, v))
print(dist[e])
```

## 조기 종료 가능

도착 노드를 pop하면 즉시 종료할 수 있다. 이 코드에서는 하지 않지만, 대규모에서 성능 향상.

## 시간/공간

- $O((V+E)\log V)$
