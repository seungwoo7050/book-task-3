# BOJ 11279 — 접근 과정

## 핵심 트릭: 부호 반전

Python `heapq`는 최소 힙만 지원. 최대 힙은 값을 음수로 넣고 꺼낼 때 다시 음수로 변환.

```python
heapq.heappush(heap, -x)  # 삽입
-heapq.heappop(heap)       # 추출
```

## 출력 최적화

매 연산마다 `print`하면 I/O 병목. `out` 리스트에 모아서 `'\n'.join(out)`으로 한 번에 출력.

## 시간/공간

- 삽입/추출 각 $O(\log N)$
- 전체 $O(N \log N)$
