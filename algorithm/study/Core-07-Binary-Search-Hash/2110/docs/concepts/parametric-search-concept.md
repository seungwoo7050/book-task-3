# 매개변수 탐색(Parametric Search) 개념 정리 — 공유기 설치

## 핵심 아이디어
"최솟값의 최댓값" 패턴 → **이진 탐색으로 답을 결정**.
결정 함수 `feasible(d)`: 최소 거리 $d$ 이상으로 $C$개 공유기를 설치할 수 있는가?

## CLRS 연결
CLRS Ch 2.3 Binary Search + 결정 문제(Decision Problem) 변환.

## 알고리즘
1. 집을 좌표순 정렬
2. `lo = 1`, `hi = max_pos - min_pos`
3. `mid = (lo + hi) / 2`로 최소 거리 후보 설정
4. `feasible(mid)` → True면 `lo = mid + 1` (더 큰 거리 시도)
5. `feasible(mid)` → False면 `hi = mid - 1`

## 결정 함수
```python
def feasible(d):
    count = 1; last = houses[0]
    for h in houses[1:]:
        if h - last >= d:
            count += 1; last = h
    return count >= C
```
그리디하게 왼쪽부터 거리 $d$ 이상인 집에 설치.
$O(N)$ 시간. 전체: $O(N \log(\text{range}))$.
