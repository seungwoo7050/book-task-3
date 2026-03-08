# 0/1 배낭 문제 개념 정리

## CLRS 연결
CLRS Ch 16.2에서 0-1 Knapsack이 그리디로 풀리지 않음을 증명.
CLRS Ch 15 Dynamic Programming으로 해결.

## 점화식
$$dp[j] = \max(dp[j],\; dp[j - w_i] + v_i) \quad \text{for } j = K \ldots w_i$$

1D 배열로 공간 최적화. 역순 순회로 0/1 성질 보장.

## 왜 역순인가?
순방향으로 순회하면 같은 아이템을 여러 번 사용 (Unbounded Knapsack).
역순이면 `dp[j-w]`가 아직 이전 아이템까지의 값이므로 0/1 보장.

## 시간/공간
| 항목 | 값 |
|------|-----|
| 시간 | $O(NK)$ |
| 공간 | $O(K)$ — 1D 최적화 |
