# BOJ 1931 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 회의실 하나에서 최대 몇 개의 회의를 할 수 있는지 구한다.
- 진행: 처음엔 "회의 시간이 짧은 것부터 선택"하면 되지 않을까 생각했다. 하지만 짧은 회의가 긴 회의 중간에 들어가면 오히려 총 개수가 줄 수 있다.
- 이슈: 핵심은 "종료 시간이 빠른 것부터 선택"하는 activity selection이다. 빨리 끝나야 다음 회의를 빨리 시작할 수 있다.
- 판단: 종료 시간 기준 정렬 → 시작 시간이 이전 종료 시간 이상이면 선택.

### Session 2
- 목표: 정렬 + 선형 스캔을 구현한다.

이 시점의 핵심 코드:

```python
meetings.sort(key=lambda x: (x[1], x[0]))

count = 0
last_end = 0
for start, end in meetings:
    if start >= last_end:
        count += 1
        last_end = end
```

처음엔 `(end, start)` 대신 `end`만으로 정렬했는데, 시작=종료인 회의(길이 0)가 있으면 순서가 달라진다. `(2,2)`와 `(1,2)`가 있을 때 `(1,2)`가 먼저 와야 `(2,2)`도 선택 가능하다.

CLI:

```bash
$ make -C study/Core-09-Greedy/1931/problem run-py
```

```text
4
```

- 다음: 시작=종료인 회의가 여러 개 연속되는 경우를 확인한다.
