# BOJ 9663 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: N×N 체스판에 N개의 퀸을 서로 공격하지 않게 놓는 경우의 수를 구한다.
- 진행: 퀸은 같은 행, 같은 열, 같은 대각선에 있으면 안 된다. 행 기준으로 한 줄씩 놓아가면 행 충돌은 자동으로 제거된다. 열과 대각선만 확인하면 된다.
- 이슈: 처음엔 모든 칸에 대해 다른 모든 퀸과의 거리를 계산하려 했는데, 그러면 매 단계 O(N)이 추가된다. 대신 "이 열을 썼는가", "이 대각선을 썼는가"를 배열로 기록하면 O(1) 체크가 가능하다.
- 판단: `col[c]`, `diag1[row-col+N-1]`, `diag2[row+col]` 세 배열을 사용한다.

### Session 2
- 목표: 백트래킹 구현을 완성한다.

이 시점의 핵심 코드:

```python
def place(row):
    nonlocal count
    if row == n:
        count += 1
        return
    for c in range(n):
        if not col[c] and not diag1[row - c + n - 1] and not diag2[row + c]:
            col[c] = diag1[row - c + n - 1] = diag2[row + c] = True
            place(row + 1)
            col[c] = diag1[row - c + n - 1] = diag2[row + c] = False
```

처음엔 대각선 인덱스 계산이 헷갈렸다. `row - col`은 같은 `/` 방향 대각선에서 같은 값을 가지고, `row + col`은 같은 `\` 방향 대각선에서 같은 값을 가진다. `row - col`이 음수가 될 수 있으니까 `+ n - 1` 오프셋을 준다.

CLI:

```bash
$ make -C study/Core-04-Recursion-Backtracking/9663/problem run-py
```

```text
92
```

(N=8일 때 92가 잘 알려진 값이라 바로 확인이 됐다.)

- 다음: 상태 복원(backtrack) 단계에서 True → False 전환이 빠짐없이 되는지 확인한다.
