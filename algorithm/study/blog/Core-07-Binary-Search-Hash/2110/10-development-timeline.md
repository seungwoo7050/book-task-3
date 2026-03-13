# BOJ 2110 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: N개의 집에 C개의 공유기를 설치하되, 가장 가까운 두 공유기 사이 거리를 최대화한다.
- 진행: 처음엔 조합을 다 시도해볼까 생각했다. 하지만 N이 최대 20만이고 C까지 고려하면 조합 수가 너무 많다.
- 이슈: "거리 D를 먼저 정하고, 그 거리로 공유기를 놓을 수 있는지 판정하는 건 어떨까?" 이 발상이 parametric search의 시작이었다.
- 판단: 가능한 거리 범위에서 이분 탐색을 하고, 각 mid에서 "최소 거리가 mid일 때 공유기 C개를 놓을 수 있는가"를 O(N)으로 판정한다.

### Session 2
- 목표: feasibility 함수와 이분 탐색 프레임을 구현한다.

이 시점의 핵심 코드:

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

처음엔 `count >= C`가 나오면 바로 리턴하지 않고 끝까지 돌았는데, 조기 종료를 넣으면 최악 케이스에서 약간 빨라진다.

- 이슈: 이분 탐색에서 `lo = mid + 1`, `hi = mid - 1`의 경계를 정확하게 잡아야 한다. feasible(mid)가 True이면 `ans = mid; lo = mid + 1`로 더 큰 거리를 시도하고, False이면 `hi = mid - 1`로 줄인다.
- 판단: "최대를 구하는 이분 탐색"이니까 feasible이 True인 마지막 값을 추적한다.

CLI:

```bash
$ make -C study/Core-07-Binary-Search-Hash/2110/problem run-py
```

```text
3
```

- 다음: 정렬을 빼먹으면 feasibility 판정이 완전히 깨진다는 걸 확인한다.
