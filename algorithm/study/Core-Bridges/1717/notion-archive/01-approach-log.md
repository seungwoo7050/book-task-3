# BOJ 1717 — 접근 과정

## Union-Find 구현

```python
def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path splitting
        x = parent[x]
    return x

def union(parent, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra == rb:
        return
    if ra < rb:
        parent[rb] = ra
    else:
        parent[ra] = rb
```

## 경로 압축: Path Splitting

`parent[x] = parent[parent[x]]` — 할아버지를 부모로 변경. 재귀적 경로 압축보다 Python에서 안전(스택 오버플로 없음).

## Union 전략

이 코드에서는 번호가 작은 쪽을 루트로 유지. 랭크 기반은 아니지만 실용적으로 충분.

## 시간/공간

- 각 연산 거의 $O(\alpha(N)) \approx O(1)$
