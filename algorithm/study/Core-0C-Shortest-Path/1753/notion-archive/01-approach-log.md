# BOJ 1753 — 접근 과정

## 다익스트라 + 힙

```python
dist = [INF] * (v + 1)
dist[k] = 0
hq = [(0, k)]
while hq:
    d, u = heapq.heappop(hq)
    if d > dist[u]:
        continue  # lazy deletion
    for nv, w in adj[u]:
        nd = d + w
        if nd < dist[nv]:
            dist[nv] = nd
            heapq.heappush(hq, (nd, nv))
```

## Lazy Deletion

`if d > dist[u]: continue` — 이미 더 나은 경로를 찾은 노드는 건너뛴다. `decrease-key` 대신 사용하는 파이썬식 패턴.

## 왜 다익스트라가 맞는가?

모든 가중치가 양수 → 한 번 확정된 최단 거리는 나중에 줄어들 수 없음 → 그리디 선택(가장 짧은 거리의 노드부터 확정)이 정당.

## 시간/공간

- $O((V+E)\log V)$
