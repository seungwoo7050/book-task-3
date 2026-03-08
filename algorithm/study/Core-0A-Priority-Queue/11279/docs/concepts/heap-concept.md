# 우선순위 큐 / 힙 개념 정리 — 최대 힙

## CLRS 연결
CLRS Ch 6 Heapsort — Max-Heap property: `A[PARENT(i)] >= A[i]`.
CLRS Ch 6.5 Priority Queue — `INSERT`, `EXTRACT-MAX`.

## Python heapq
Python `heapq`는 **최소 힙**만 지원.
최대 힙은 값을 **부호 반전**(`-x`)하여 구현:
```python
heapq.heappush(heap, -x)    # 삽입
-heapq.heappop(heap)         # 최대값 추출
```

## 연산 복잡도
| 연산 | 시간 |
|------|------|
| INSERT | $O(\log N)$ |
| EXTRACT-MAX | $O(\log N)$ |
| BUILD-HEAP | $O(N)$ |
