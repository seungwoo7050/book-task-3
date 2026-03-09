# BOJ 2750 — 접근 과정

## 구현

```python
nums = [int(input()) for _ in range(N)]
nums.sort()
print('\n'.join(map(str, nums)))
```

Python의 Timsort는 $O(N \log N)$ 보장. $N \leq 1000$에서 어떤 정렬 알고리즘이든 충분.

## 대안으로 고려한 것

- **삽입 정렬 직접 구현**: CLRS Ch 2.1의 학습 목적으로 가능. $O(N^2)$이지만 $N \leq 1000$에서 문제 없음.
- **병합 정렬**: Ch 2.3의 분할 정복 예시. 재귀 + 병합으로 $O(N \log N)$.
- **힙 정렬**: Ch 6의 in-place $O(N \log N)$.

학습 목적으로 직접 구현을 해볼 수 있지만, 제출용으로는 내장 `sort()`가 가장 간결하고 확실하다.
