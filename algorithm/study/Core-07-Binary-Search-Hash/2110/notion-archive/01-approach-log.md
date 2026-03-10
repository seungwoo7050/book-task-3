# BOJ 2110 — 접근 과정: 답에 대한 이진 탐색

## 핵심 아이디어

"최소 거리 $d$로 $C$개의 공유기를 설치할 수 있는가?"를 판별 함수로 정의하고, $d$에 대해 이진 탐색한다.

## 판별 함수

```python
def feasible(d):
    count = 1
    last = houses[0]
    for i in range(1, N):
        if houses[i] - last >= d:
            count += 1
            last = houses[i]
            if count >= C:
                return True
    return False
```

탐욕적으로 가능한 한 빨리 설치: 현재 위치에서 거리 $d$ 이상인 첫 집에 설치. $O(N)$.

## 이진 탐색

```python
lo, hi, ans = 1, houses[-1] - houses[0], 0
while lo <= hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        ans = mid
        lo = mid + 1  # 더 큰 거리도 가능?
    else:
        hi = mid - 1  # 거리 줄이기
```

## 전체 복잡도

- 정렬: $O(N \log N)$
- 이진 탐색: $O(\log(\text{max\_coord}) \cdot N)$
- 전체: $O(N \log N + N \log(\text{max\_coord}))$

## 왜 탐욕적 판별이 정당한가

집이 정렬되어 있으므로, "가능한 한 빨리 설치"하는 것이 설치 개수를 최대화한다. 뒤에서 더 많이 설치할 수 있는 여지를 희생할 이유가 없다.
