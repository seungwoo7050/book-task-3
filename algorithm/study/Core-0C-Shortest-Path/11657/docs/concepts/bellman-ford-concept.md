# 벨만-포드 개념 정리 — 타임머신

## CLRS 연결
CLRS Ch 24.1 Bellman-Ford Algorithm.

## 핵심 아이디어
음의 가중치 간선이 있을 때의 단일 출발점 최단 경로.
$V-1$번 모든 간선을 완화(relax). $V$번째에도 완화가 발생하면 **음의 사이클 존재**.

## 알고리즘
```
for i = 1 to V-1:
    for (a, b, c) in edges:
        if dist[a] + c < dist[b]:
            dist[b] = dist[a] + c

// V번째 검사
for (a, b, c) in edges:
    if dist[a] + c < dist[b]:
        → 음의 사이클!
```

## 복잡도
$O(VE)$ — 다익스트라보다 느리지만 음의 가중치 처리 가능.
