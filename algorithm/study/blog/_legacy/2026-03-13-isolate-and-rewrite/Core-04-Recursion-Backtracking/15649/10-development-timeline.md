# BOJ 15649 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: 1부터 N까지 수 중에서 M개를 고른 순열을 사전순으로 출력한다.
- 진행: 순열이니까 순서가 다르면 다른 출력이다. 조합이 아니라 순열이라는 걸 확인했다.
- 이슈: M개를 고르는 순열의 수가 N!/(N-M)!이니까 N=8이면 최대 40320개. 충분히 탐색 가능하다.
- 판단: 선택/해제를 반복하는 백트래킹으로 구현한다.

### Session 2
- 목표: 백트래킹을 구현한다.

이 시점의 핵심 코드:

```python
def backtrack(depth):
    if depth == m:
        out.append(' '.join(map(str, seq)))
        return
    for i in range(1, n + 1):
        if not used[i]:
            used[i] = True
            seq.append(i)
            backtrack(depth + 1)
            seq.pop()
            used[i] = False
```

처음엔 `used` 배열 없이 `if i not in seq`로 체크했는데, 리스트 in 연산이 O(M)이라 느릴 수 있다. boolean 배열이면 O(1)이다.

CLI:

```bash
$ make -C study/Core-04-Recursion-Backtracking/15649/problem run-py
```

```text
1 2
1 3
1 4
2 1
...
```

- 다음: 출력을 한 번에 모아서 쓰는 게 줄마다 print하는 것보다 빠른지 확인한다.
