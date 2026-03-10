# BOJ 1149 — 접근 과정: 3-상태 점화식

## 상태 정의

$\textrm{dp}[i][c]$ = $i$번 집까지 칠했을 때, $i$번 집의 색이 $c$일 때의 최소 비용

## 점화식

$$\textrm{dp}[i][c] = \textrm{cost}[i][c] + \min(\textrm{dp}[i-1][c'] \mid c' \neq c)$$

즉, 현재 집을 색 $c$로 칠하려면, 이전 집은 $c$가 아닌 나머지 두 색 중 최소 비용인 것을 선택.

## 공간 최적화

$\textrm{dp}[i]$는 $\textrm{dp}[i-1]$에만 의존하므로, 2D 배열 대신 **이전 행 변수 3개**만 유지:

```python
prev = list(map(int, input().split()))  # 첫 번째 집
for _ in range(N - 1):
    cost = list(map(int, input().split()))
    curr = [
        cost[0] + min(prev[1], prev[2]),
        cost[1] + min(prev[0], prev[2]),
        cost[2] + min(prev[0], prev[1]),
    ]
    prev = curr
print(min(prev))
```

$O(N)$ 시간, $O(1)$ 공간 (상수 3개).

## 왜 그리디가 안 되는가

"매 집에서 가장 싼 색을 선택"하면 인접 제약을 만족하지 못하거나, 전체 최소를 놓칠 수 있다. DP가 필요한 이유.
