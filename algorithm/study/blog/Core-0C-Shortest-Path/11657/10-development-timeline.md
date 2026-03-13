# BOJ 11657 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 음수 가중치 간선이 있는 그래프에서 최단 경로를 구한다. 음수 사이클이 있으면 -1을 출력한다.
- 진행: Dijkstra를 먼저 생각했는데, 음수 간선이 있으면 Dijkstra가 정확하지 않다.
- 이슈: Bellman-Ford를 써야 한다. V-1번 모든 간선을 완화(relax)하고, V번째에도 완화가 일어나면 음수 사이클이 있다는 뜻이다.
- 판단: 간선 리스트를 만들고 N-1회 반복 완화 + 1회 추가 검사로 구현한다.

### Session 2
- 목표: Bellman-Ford를 구현한다.

이 시점의 핵심 코드:

```python
dist = [INF] * (n + 1)
dist[1] = 0
for i in range(n):
    for a, b, c in edges:
        if dist[a] != INF and dist[a] + c < dist[b]:
            if i == n - 1:
                print(-1)
                return
            dist[b] = dist[a] + c
```

처음엔 `dist[a] != INF` 체크를 빼먹었다. 시작점에서 도달 불가능한 노드의 dist가 INF인 상태에서 음수 간선을 더하면 INF보다 작은 값이 되어 잘못된 완화가 일어난다.

CLI:

```bash
$ make -C study/Core-0C-Shortest-Path/11657/problem run-py
```

```text
4
-1
```

- 다음: 음수 사이클 검출이 시작점에서 도달 가능한 사이클만 잡는지 확인한다.
