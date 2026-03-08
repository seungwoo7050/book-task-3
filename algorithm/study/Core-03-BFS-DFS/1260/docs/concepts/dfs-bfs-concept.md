# DFS와 BFS 비교 개념 정리

## DFS (깊이 우선 탐색) — CLRS Ch 22.3

### 핵심 아이디어
가능한 한 **깊이** 들어간 뒤, 막히면 백트래킹.

### 자료구조
- **재귀** (암묵적 스택) 또는 **명시적 스택**

### 의사코드
```
DFS-VISIT(G, u)
  u.color = GRAY
  for each v ∈ G.Adj[u]
    if v.color == WHITE
      DFS-VISIT(G, v)
  u.color = BLACK
```

### 특성
- DFS 트리/숲 생성
- 간선 분류 (tree, back, forward, cross)
- 위상 정렬, SCC, 사이클 검출에 활용

## BFS (너비 우선 탐색) — CLRS Ch 22.2

### 핵심 아이디어
시작점에서 **가까운** 정점부터 레벨 단위로 탐색.

### 자료구조
- **큐(Queue)**

### 의사코드
```
BFS(G, s)
  s.color = GRAY
  s.d = 0
  Q = {s}
  while Q ≠ ∅
    u = DEQUEUE(Q)
    for each v ∈ G.Adj[u]
      if v.color == WHITE
        v.color = GRAY
        v.d = u.d + 1
        ENQUEUE(Q, v)
    u.color = BLACK
```

### 특성
- **최단 경로** (비가중치 그래프)
- 레벨 단위 탐색
- `visited`를 큐 삽입 시점에 체크해야 중복 방지

## DFS vs BFS 비교

| 항목 | DFS | BFS |
|------|-----|-----|
| 자료구조 | 스택 (재귀) | 큐 |
| 탐색 순서 | 깊이 우선 | 너비 우선 |
| 최단 경로 | X | O (비가중치) |
| 복잡도 | $O(V+E)$ | $O(V+E)$ |
| 메모리 | $O(V)$ (스택) | $O(V)$ (큐) |
| 활용 | 위상정렬, SCC | 최단경로, 레벨탐색 |

## 이 문제에서의 적용

같은 그래프에서 DFS와 BFS를 모두 수행:
- 인접 리스트 오름차순 정렬 → 결정적 순서 보장
- `visited` 배열을 탐색마다 독립적으로 초기화
- DFS 결과와 BFS 결과를 비교하면 탐색 특성 차이가 명확
