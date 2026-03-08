# 최소 힙 개념 정리

## CLRS 연결
CLRS Ch 6.5 Priority Queue — `INSERT`, `EXTRACT-MIN`.
Min-Heap property: `A[PARENT(i)] <= A[i]`.

## Python heapq
`heapq`는 기본이 최소 힙이므로 그대로 사용:
```python
heapq.heappush(heap, x)
heapq.heappop(heap)
```

## 최대 힙과의 차이
최대 힙은 부호 반전이 필요하지만, 최소 힙은 직접 사용 가능.
