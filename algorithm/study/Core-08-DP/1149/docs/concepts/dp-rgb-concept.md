# DP 개념 정리 — RGB거리

## CLRS 연결
CLRS Ch 15 Dynamic Programming — 최적 부분 구조 + 중복 부분 문제.

## 점화식
$$dp[i][c] = cost[i][c] + \min_{c' \neq c} dp[i-1][c']$$

세 가지 색상 중 인접 집과 다른 색을 선택하여 최소 비용.

## 공간 최적화
이전 행(`prev`)만 필요하므로 $O(1)$ 추가 공간 (3개 변수).
2D 배열 대신 `prev = [R, G, B]`만 유지.

## 시간 복잡도
$O(N)$ — 각 집에서 상수(3×2) 연산.
