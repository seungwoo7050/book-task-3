# BOJ 1927 — 접근 과정

## 핵심

```python
if x:
    heapq.heappush(heap, x)
else:
    out.append(str(heapq.heappop(heap)) if heap else '0')
```

11279와의 차이: 부호 반전이 필요 없다. `heapq`가 기본 최소 힙이므로 그대로 사용.

## 출력 최적화

`sys.stdout.write('\n'.join(out) + '\n')` — 한 번에 출력.

## 시간/공간

- $O(N \log N)$
