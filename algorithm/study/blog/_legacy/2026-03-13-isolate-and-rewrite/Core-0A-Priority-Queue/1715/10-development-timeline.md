# BOJ 1715 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: N묶음의 카드를 하나로 합칠 때, 비교 횟수의 최소 합을 구한다.
- 진행: 처음엔 그냥 순서대로 합치면 안 되나 생각했다. 그런데 큰 묶음을 먼저 합치면 그 비용이 뒤의 모든 합치기에 계속 누적된다.
- 이슈: 핵심 관찰은 "가장 작은 두 묶음을 먼저 합치면 전체 비용이 최소"라는 것이다. Huffman 인코딩과 같은 원리다.
- 판단: 최소 힙을 써서 가장 작은 둘을 꺼내고, 합을 다시 넣는 걸 반복한다.

### Session 2
- 목표: Huffman-style greedy를 구현한다.

이 시점의 핵심 코드:

```python
heapq.heapify(heap)
total = 0
while len(heap) > 1:
    a = heapq.heappop(heap)
    b = heapq.heappop(heap)
    s = a + b
    total += s
    heapq.heappush(heap, s)
```

처음엔 "합친 결과를 왜 다시 힙에 넣지?"라는 의문이 있었다. 합친 묶음은 다음 합치기의 피연산자가 되기 때문이다. 넣지 않으면 최종 하나로 합쳐지지 않는다.

CLI:

```bash
$ make -C study/Core-0A-Priority-Queue/1715/problem run-py
```

```text
100
```

- 다음: N=1이면 합칠 묶음이 없으니 답이 0인지 확인한다.
