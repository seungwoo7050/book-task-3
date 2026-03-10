# BOJ 12865 — 접근 과정: 1D 배열 역순 순회

## 2D DP 원형

$\textrm{dp}[i][j]$ = 처음 $i$개 물건으로 용량 $j$인 배낭을 채울 때의 최대 가치

점화식:
$$\textrm{dp}[i][j] = \max(\textrm{dp}[i-1][j],\ \textrm{dp}[i-1][j - w_i] + v_i)$$

$O(NK)$ 시간, $O(NK)$ 공간.

## 1D 최적화

$\textrm{dp}[i]$는 $\textrm{dp}[i-1]$에만 의존. 1D 배열로 축소:

```python
dp = [0] * (K + 1)
for _ in range(N):
    w, v = map(int, input().split())
    for j in range(K, w - 1, -1):
        dp[j] = max(dp[j], dp[j - w] + v)
```

**역순 순회가 핵심**: 순방향으로 돌면 같은 아이템을 여러 번 넣는 효과가 생긴다 (이것은 완전 배낭 문제). 역순이면 각 아이템이 한 번만 사용된다.

## 왜 역순인가?

`dp[j - w]`를 참조할 때, 이 값이 "현재 아이템을 아직 고려하지 않은" 상태여야 한다. 역순이면 `j - w < j`이므로 아직 갱신되지 않은 값을 참조한다.

## 시간/공간

- $O(NK)$ 시간, $O(K)$ 공간
