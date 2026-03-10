# 0x14 Network Flow — 접근 과정

## Edmonds-Karp: BFS 기반 증가 경로

1. BFS로 $s \to t$ 경로 탐색 (잔여 용량 > 0인 간선만)
2. 경로 상 최소 잔여 용량 = bottleneck
3. 경로 상 모든 간선: 순방향 용량 감소, 역방향 용량 증가
4. 반복 — BFS 실패 시 종료

```python
cap[u][v] -= bn
cap[v][u] += bn
```

## 용량 행렬 vs 인접 리스트

`cap[][]`로 잔여 용량 관리, `adj[]`로 BFS 탐색. 역간선은 입력 시 양방향으로 adj에 추가.

## 최대 유량 정리

max-flow = min-cut (Ford-Fulkerson 정리).
