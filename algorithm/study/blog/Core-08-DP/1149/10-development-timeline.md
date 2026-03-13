# BOJ 1149 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: N개의 집을 R/G/B로 칠하되, 인접한 집은 다른 색이어야 하고, 비용 합을 최소화한다.
- 진행: 처음엔 그리디로 "매번 가장 싼 색"을 고르면 되지 않을까 생각했다. 하지만 현재 집에서 싼 색을 고르면 다음 집에서 비싼 색만 남을 수 있다.
- 이슈: 그리디는 안 된다. DP로 "i번째 집을 색 c로 칠했을 때의 최소 누적 비용"을 기록해야 한다.
- 판단: `prev[c]`를 이전 집까지의 최소 비용으로 두고, 매 집마다 3색 각각에 대해 "나머지 두 색 중 최소 + 현재 비용"으로 갱신한다.

### Session 2
- 목표: DP를 구현한다.

이 시점의 핵심 코드:

```python
prev = list(map(int, input().split()))

for _ in range(N - 1):
    cost = list(map(int, input().split()))
    curr = [
        cost[0] + min(prev[1], prev[2]),
        cost[1] + min(prev[0], prev[2]),
        cost[2] + min(prev[0], prev[1]),
    ]
    prev = curr

print(min(prev))
```

2차원 DP 표를 만들 수도 있지만, 현재 행은 이전 행의 값만 참조하니까 `prev` 하나로 공간을 절약할 수 있다. 처음엔 2차원 배열로 풀었다가, 나중에 이 패턴을 알고 줄였다.

CLI:

```bash
$ make -C study/Core-08-DP/1149/problem run-py
```

```text
96
```

- 다음: 첫 번째 집의 비용을 prev 초기값으로 직접 읽는 구현이 맞는지 확인한다.
