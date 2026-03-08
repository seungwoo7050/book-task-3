# 다익스트라 개념 정리 — 최소비용 구하기

## CLRS 연결
CLRS Ch 24.3 Dijkstra's Algorithm.

## 핵심 아이디어
음이 아닌 가중치 그래프에서 단일 출발점 최단 경로.
우선순위 큐(최소 힙)로 가장 가까운 확정 안 된 노드를 선택.

## 알고리즘
```
dist[s] = 0, 나머지 INF
while 힙이 비지 않으면:
    (d, u) = extract_min
    if d > dist[u]: skip (lazy deletion)
    for (v, w) in adj[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            push (dist[v], v)
```

## 복잡도
$O((V + E) \log V)$ — 이진 힙 사용 시.
