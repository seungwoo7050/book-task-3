# BOJ 1167 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 가중치 트리에서 지름(가장 먼 두 노드 사이 거리)을 구한다.
- 진행: 처음엔 모든 노드 쌍의 거리를 구하려 했다. O(V²)인데 V가 최대 10만이라 10억 연산... 안 된다.
- 이슈: 트리 지름을 구하는 알려진 방법이 있다고 어디선가 본 기억이 있다. "임의의 점에서 가장 먼 점을 찾고, 그 점에서 다시 가장 먼 점을 찾으면 그 거리가 지름"이라는 two-pass BFS.
- 판단: 직관적으로는 "끝점 하나를 찾고, 거기서 반대쪽 끝점을 찾는다"인데, 왜 이게 맞는지는 증명을 완전히 이해하지는 않았다. 다만 트리에서 경로가 유일하다는 성질 때문에 성립한다는 건 납둑이 됐다.

### Session 2
- 목표: two-pass BFS를 구현한다.

이 시점의 핵심 코드:

```python
def bfs(start):
    dist = [-1] * (v + 1)
    dist[start] = 0
    q = deque([start])
    far_node, far_dist = start, 0
    while q:
        u = q.popleft()
        for nv, w in adj[u]:
            if dist[nv] == -1:
                dist[nv] = dist[u] + w
                q.append(nv)
                if dist[nv] > far_dist:
                    far_dist = dist[nv]
                    far_node = nv
    return far_node, far_dist

u, _ = bfs(1)
_, diameter = bfs(u)
```

처음엔 BFS에서 가중치를 다루려면 Dijkstra가 필요하다고 생각했다. 하지만 트리에서는 경로가 유일하니까 BFS로 충분하다. 가중치를 누적만 하면 된다.

CLI:

```bash
$ make -C study/Core-0B-Graph-Tree/1167/problem run-py
```

```text
11
```

- 다음: 입력 파싱이 `-1`로 끝나는 형태라서 정확히 구현됐는지 확인한다.
