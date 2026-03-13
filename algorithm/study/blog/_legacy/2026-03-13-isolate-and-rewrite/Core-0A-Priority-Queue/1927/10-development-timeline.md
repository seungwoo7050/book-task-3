# BOJ 1927 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 최소 힙을 구현한다. 자연수를 넣거나, 0이면 최솟값을 꺼내 출력한다.
- 진행: Python의 `heapq` 모듈이 기본적으로 min-heap이니까 그대로 사용하면 된다.
- 이슈: 힙이 비어 있는데 0이 들어오면 0을 출력해야 한다.
- 판단: `heappush`, `heappop`, 빈 힙 체크만으로 구현 가능하다.

### Session 2
- 목표: 구현을 완성한다.

이 시점의 핵심 코드:

```python
for _ in range(n):
    x = int(input())
    if x:
        heapq.heappush(heap, x)
    else:
        out.append(str(heapq.heappop(heap)) if heap else '0')
```

처음엔 x==0일 때의 분기를 복잡하게 썼는데, 삼항 연산자로 한 줄에 정리하니 깔끔해졌다.

CLI:

```bash
$ make -C study/Core-0A-Priority-Queue/1927/problem run-py
```

```text
0
1
2
```

- 다음: N이 최대 10만이라 매번 print하면 느린지 확인한다.
