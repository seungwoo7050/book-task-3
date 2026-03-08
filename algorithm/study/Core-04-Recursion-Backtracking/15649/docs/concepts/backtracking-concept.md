# 백트래킹(Backtracking) 개념 정리

## 정의

**백트래킹**은 해를 구성하는 과정에서 유망하지 않은 경로를 조기에 포기(가지치기)하고
이전 단계로 되돌아가는 탐색 기법이다.

## 핵심 패턴: 선택 → 재귀 → 복원

```python
def backtrack(depth):
    if depth == target:
        process(current_state)
        return
    for candidate in candidates:
        if is_valid(candidate):
            choose(candidate)      # 선택
            backtrack(depth + 1)   # 재귀
            unchoose(candidate)    # 복원 (상태 원복)
```

## 순열 생성에서의 적용

$\{1, \ldots, N\}$에서 $M$개를 중복 없이 선택:

```python
used = [False] * (n + 1)
seq = []

def backtrack(depth):
    if depth == m:
        print(seq)
        return
    for i in range(1, n + 1):
        if not used[i]:
            used[i] = True; seq.append(i)
            backtrack(depth + 1)
            seq.pop(); used[i] = False
```

## 시간 복잡도

순열: $P(N, M) = \frac{N!}{(N-M)!}$

$N = 8, M = 8$이면 $8! = 40{,}320$개. 완전 탐색 가능.

## CLRS 연결

CLRS Ch 4의 재귀 패러다임을 확장하여,
"모든 가능한 해를 체계적으로 탐색"하는 기법.
상태 공간 트리(State Space Tree)를 DFS로 순회한다.

## 가지치기(Pruning)

- `used[i]` 체크: 이미 선택한 원소 재선택 방지
- N-Queen: 행/열/대각선 충돌 체크
- 조합 최적화: 하한 체크 (Branch and Bound)
