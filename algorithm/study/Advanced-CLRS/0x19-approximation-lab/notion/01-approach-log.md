# 0x19 Approximation Lab — 접근 과정

## Greedy Set Cover

1. 미커버 원소 집합 유지
2. 매 단계, 가장 많은 미커버 원소를 포함하는 집합 선택 (동률 시 결정적 타이브레이킹)
3. 선택된 집합의 원소를 커버 처리
4. 전체 커버될 때까지 반복

근사 비율: $O(\ln n)$ — 최적의 $\ln n$ 배 이내.

## 2-Approximation Vertex Cover

1. 미커버 간선 중 하나 선택 $(u, v)$
2. $u$와 $v$ 모두 커버에 추가
3. $u$ 또는 $v$에 인접한 모든 간선 제거
4. 반복

근사 비율: 2 — 최적의 2배 이내.

```python
while uncovered_edges:
    u, v = pick_edge()  # deterministic tie-breaking
    cover.add(u)
    cover.add(v)
    remove edges incident to u or v
```
