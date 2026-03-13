# BOJ 2170 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 수직선 위에 선분들을 긋고, 그려진 총 길이를 구한다.
- 진행: 처음엔 선분마다 배열에 칠하는 방식을 생각했다. 그런데 좌표 범위가 -10억~10억이라 배열로는 불가능하다.
- 이슈: "구간을 정렬한 뒤 겹치는 것끼리 병합하면 되지 않을까?" 라는 가설을 세웠다.
- 판단: 시작점 기준 정렬 → 현재 구간과 다음 구간의 겹침 여부 확인 → 겹치면 확장, 안 겹치면 확정. 이게 interval merge 패턴이다.

### Session 2
- 목표: interval merge를 구현한다.

이 시점의 핵심 코드:

```python
segments.sort()
total = 0
cur_start, cur_end = segments[0]

for s, e in segments[1:]:
    if s <= cur_end:
        cur_end = max(cur_end, e)
    else:
        total += cur_end - cur_start
        cur_start, cur_end = s, e

total += cur_end - cur_start
```

처음엔 마지막 구간을 루프 밖에서 따로 더해야 한다는 걸 빠뜨렸다. 루프는 "다음 구간이 빈 간격을 만들 때"만 현재 구간을 확정하니까, 맨 마지막 구간은 루프 안에서 확정되지 않는다.

CLI:

```bash
$ make -C study/Core-06-Sorting/2170/problem run-py
```

```text
5
```

- 다음: "맞닿는 구간"을 겹침으로 처리하는지 확인한다. `s <= cur_end`에서 `<=`가 맞닿음을 포함한다.
