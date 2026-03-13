# BOJ 2252 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 학생들의 키 순서 관계가 주어질 때, 줄을 세운 순서를 출력한다.
- 진행: "A가 B 앞에 서야 한다"는 관계가 여러 개 주어지니까, 이건 방향 그래프의 위상 정렬이다.
- 이슈: 위상 정렬 구현 방법은 두 가지 — Kahn(BFS, 진입차수) 또는 DFS 기반. Kahn이 더 직관적이라 이걸 골랐다.
- 판단: 진입차수가 0인 노드를 큐에 넣고, 꺼내면서 인접 노드의 진입차수를 줄이고, 0이 되면 큐에 넣는다.

### Session 2
- 목표: Kahn 알고리즘을 구현한다.

이 시점의 핵심 코드:

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

처음엔 "진입차수가 0인 노드가 여러 개이면 어떤 걸 먼저 꺼내나?"가 걱정이었다. 이 문제는 "답이 여러 개이면 아무거나 출력"하면 되기 때문에 큐 순서는 상관없다.

CLI:

```bash
$ make -C study/Core-0D-MST-Topo/2252/problem run-py
```

```text
3 2 1
```

- 다음: 사이클이 있으면(모든 노드를 방문하지 못하면) 어떻게 되는지 확인한다.
