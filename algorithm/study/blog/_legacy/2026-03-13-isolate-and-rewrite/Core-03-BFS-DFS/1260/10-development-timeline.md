# BOJ 1260 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 같은 그래프에서 DFS와 BFS를 수행하고 방문 순서를 출력한다.
- 진행: 인접 리스트를 구성하고, 작은 번호부터 방문하라는 조건이 있으니까 인접 리스트를 정렬해야 한다.
- 이슈: DFS를 재귀로 구현하면 Python의 재귀 제한(기본 1000)에 걸릴 수 있다. N이 최대 1000이라 setrecursionlimit을 올려야 한다.
- 판단: DFS는 재귀, BFS는 deque 큐로 구현한다.

### Session 2
- 목표: DFS와 BFS를 구현한다.

이 시점의 핵심 코드 — DFS:

```python
def dfs(u):
    visited[u] = True
    dfs_order.append(u)
    for w in adj[u]:
        if not visited[w]:
            dfs(w)
```

BFS:

```python
q = deque([v])
visited[v] = True
while q:
    u = q.popleft()
    bfs_order.append(u)
    for w in adj[u]:
        if not visited[w]:
            visited[w] = True
            q.append(w)
```

BFS에서 visited를 큐에 넣을 때 마킹하는 게 중요하다. popleft할 때 마킹하면 같은 노드가 여러 번 큐에 들어간다. 처음엔 그 차이를 모르고 popleft 시점에 마킹했다가 방문 순서가 달라졌다.

CLI:

```bash
$ make -C study/Core-03-BFS-DFS/1260/problem run-py
```

```text
1 2 4 3
1 2 3 4
```

- 다음: 양방향 간선이라 `adj[a].append(b); adj[b].append(a)` 양쪽 처리가 되는지 확인한다.
