# DFS(깊이 우선 탐색) 개념 정리

## 정의

**DFS(Depth-First Search)**는 그래프 탐색 알고리즘으로,
가능한 한 깊이 들어간 뒤 더 이상 진행할 수 없으면 백트래킹한다.

## CLRS 연결 (Ch 22.3)

### 의사코드

```
DFS(G)
  for each vertex u ∈ G.V
    u.color = WHITE
    u.π = NIL
  time = 0
  for each vertex u ∈ G.V
    if u.color == WHITE
      DFS-VISIT(G, u)

DFS-VISIT(G, u)
  time = time + 1
  u.d = time           ← 발견 시간
  u.color = GRAY
  for each v ∈ G.Adj[u]
    if v.color == WHITE
      v.π = u
      DFS-VISIT(G, v)
  u.color = BLACK
  time = time + 1
  u.f = time           ← 종료 시간
```

### 핵심 속성
- **발견 시간 `d[u]`**: 정점을 처음 방문한 시각 → 이 문제의 "방문 순서"
- **종료 시간 `f[u]`**: 정점의 모든 후손 탐색 완료 시각
- **색상**: WHITE(미방문) → GRAY(탐색 중) → BLACK(완료)
- **시간 복잡도**: $\Theta(V + E)$

### 간선 분류
DFS는 간선을 4종류로 분류한다:
1. **Tree edge**: DFS 트리의 간선
2. **Back edge**: 조상으로 돌아가는 간선 (사이클 존재 증거)
3. **Forward edge**: 후손으로 가는 비트리 간선
4. **Cross edge**: 나머지

## 이 문제에서의 적용

- 시작점 $R$에서 DFS 수행
- 인접 정점을 **오름차순** 정렬하여 결정적 방문 순서 보장
- `d[u]` (발견 시간) = 방문 순서
- 미방문 정점은 0 출력

## Python 주의사항

```python
sys.setrecursionlimit(200000)
```
Python 기본 재귀 한도는 1000. $N = 100{,}000$이면 반드시 증가시켜야 한다.
또는 스택 기반 반복 DFS로 변환할 수 있다.
