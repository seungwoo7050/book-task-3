# BOJ 1920 — 접근 과정: set vs 이진 탐색

## 해시 셋 방식 (채택)

```python
A = set(map(int, input().split()))
for q in queries:
    out.append('1' if q in A else '0')
```

`set`의 `in` 연산은 평균 $O(1)$. 전체 $O(N + M)$.

## 이진 탐색 방식 (대안)

```python
A.sort()
for q in queries:
    # bisect_left로 이진 탐색
    idx = bisect_left(A, q)
    found = idx < len(A) and A[idx] == q
```

정렬 $O(N \log N)$ + 쿼리 $O(M \log N)$.

## 선택 이유

Python에서는 `set`이 더 간결하고 빠르다. C++에서는 `unordered_set`(해시)이나 `lower_bound`(이진 탐색) 모두 좋은 선택.

## 출력 최적화

$M$개 결과를 `'\n'.join`으로 한 번에 출력.
