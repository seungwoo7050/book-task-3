# BOJ 15649 — 접근 과정: 백트래킹 패턴 확립

## 핵심 구조

백트래킹의 3단계 패턴:
1. **선택**: `used[i] = True`, `seq.append(i)`
2. **재귀**: `backtrack(depth + 1)`
3. **되돌림**: `seq.pop()`, `used[i] = False`

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

## 사전순 보장

`range(1, n + 1)`로 1부터 오름차순으로 시도하므로, 별도 정렬 없이 사전순이 보장된다. DFS가 본질적으로 사전순 탐색 트리를 생성한다.

## 출력 최적화

모든 순열을 `out` 리스트에 모아서 `'\n'.join(out)`으로 한 번에 출력한다. $P(8,8) = 40320$줄을 개별 `print`하면 I/O 오버헤드가 크다.

## 대안으로 고려한 것

- **itertools.permutations**: `itertools.permutations(range(1, n+1), m)` — 한 줄이면 되지만 백트래킹 학습이 목적이므로 부적절
- **비트마스크**: `used` 배열 대신 정수 비트로 선택 관리. $N \leq 8$이므로 적합하지만, 가독성을 위해 배열 방식 채택

## DFS 트리 시각화

$N = 3, M = 2$ 예시:
```
root
├── 1 → {1,2}, {1,3}
├── 2 → {2,1}, {2,3}
└── 3 → {3,1}, {3,2}
```

이 트리의 리프가 곧 출력 순열이다.
