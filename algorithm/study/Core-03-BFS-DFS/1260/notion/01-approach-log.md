# 접근 로그

> 프로젝트: DFS와 BFS
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 그래프 표현 선택

인접 행렬과 인접 리스트 중 고민했다. $N \leq 1000$이므로 인접 행렬도 가능하지만, 간선이 적을 때 비효율적이다. 인접 리스트로 결정하되, "번호가 작은 정점 먼저 방문" 조건을 위해 각 리스트를 **정렬**하기로 했다.

## DFS 구현: 재귀 방식

CLRS의 DFS-VISIT 의사코드를 거의 그대로 옮겼다. `visited` 배열로 방문 여부를 관리하고, 재귀 호출로 깊이 우선 탐색한다. Python의 기본 재귀 한도가 1000이므로 `sys.setrecursionlimit(10000)`을 설정했다.

```python
def dfs(u):
    visited[u] = True
    dfs_order.append(u)
    for w in adj[u]:
        if not visited[w]:
            dfs(w)
```

명시적 스택 방식도 고려했지만, 이 문제의 $N$ 범위에서는 재귀가 충분하고 코드가 더 직관적이다.

## BFS 구현: deque 활용

`collections.deque`를 사용해 FIFO 큐를 구현했다. BFS의 핵심은 큐에 넣을 때 즉시 방문 표시를 하는 것이다. "꺼낼 때 방문 표시"를 하면 같은 정점이 중복 삽입되는 문제가 생긨다.

```python
q = deque([v])
visited[v] = True
while q:
    u = q.popleft()
    for w in adj[u]:
        if not visited[w]:
            visited[w] = True
            q.append(w)
```

## 핵심 설계 결정

1. **인접 리스트 정렬**: 입력 후 한 번만 정렬하면 DFS, BFS 모두에서 번호 순 방문이 보장된다
2. **visited 배열 분리**: DFS와 BFS에서 각각 새로운 visited 배열을 사용해야 한다. 같은 배열을 재사용하면 BFS가 이미 방문된 정점을 건너뛴다
3. **결과 수집 후 출력**: 리스트에 모아서 `' '.join`으로 한 번에 출력

## 대안으로 고려한 것

- 명시적 스택 DFS: 코드가 길어지고, 방문 순서가 달라질 수 있어 재귀 방식 채택
- 인접 행렬: $N \leq 1000$에서 $O(N^2)$ 공간은 허용되지만 불필요
