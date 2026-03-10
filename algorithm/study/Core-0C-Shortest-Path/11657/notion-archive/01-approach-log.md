# BOJ 11657 — 접근 과정

## 벨만-포드 알고리즘

$V-1$번 모든 간선을 순회하며 relaxation. $V$번째에도 갱신이 일어나면 음의 사이클.

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

## 핵심 포인트

1. $V-1$번 반복: 최단 경로는 최대 $V-1$개 간선을 포함
2. $V$번째 갱신 = 음의 사이클: 이미 최적인데 더 줄어든다면 무한히 줄어들 수 있음
3. `dist[a] != INF` 검사: 아직 도달 불가한 정점에서 출발하는 relaxation 방지

## 다익스트라와의 차이

- 다익스트라: 음의 가중치 불가, $O((V+E)\log V)$
- 벨만-포드: 음의 가중치 OK, $O(VE)$

## 시간/공간

- $O(VE)$
