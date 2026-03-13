# BOJ 1753 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 방향 그래프에서 시작점으로부터 모든 정점까지의 최단 거리를 구한다. 가중치는 양수(1~10).
- 진행: 양수 가중치 + 단일 시작점 → Dijkstra.
- 이슈: 우선순위 큐 없이 매번 최소 거리 노드를 찾으면 O(V²)인데, V가 최대 2만이라 가능할 수도 있다. 하지만 간선이 30만개까지이니 heapq 기반 O((V+E) log V)가 안전하다.
- 판단: heapq를 사용한 Dijkstra를 구현한다.

### Session 2
- 목표: Dijkstra를 구현한다.

이 시점의 핵심 코드:

```python
dist = [INF] * (v + 1)
dist[k] = 0
hq = [(0, k)]
while hq:
    d, u = heapq.heappop(hq)
    if d > dist[u]:
        continue
    for nv, w in adj[u]:
        nd = d + w
        if nd < dist[nv]:
            dist[nv] = nd
            heapq.heappush(hq, (nd, nv))
```

`if d > dist[u]: continue` — 이 한 줄이 lazy deletion이다. 같은 노드가 여러 번 힙에 들어갈 수 있는데, 이미 더 짧은 경로로 처리된 노드는 건너뛴다. 처음엔 이걸 빼먹었다가 같은 노드를 여러 번 처리하는 버그가 났다.

CLI:

```bash
$ make -C study/Core-0C-Shortest-Path/1753/problem run-py
```

```text
0
2
3
7
INF
```

- 다음: 도달 불가능한 노드에 "INF"를 출력하는 처리가 맞는지 확인한다.
