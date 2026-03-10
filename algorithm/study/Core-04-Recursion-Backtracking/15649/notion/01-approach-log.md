# 접근 로그

> 프로젝트: N과 M (1)
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

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

## 이 접근에서 꼭 기억할 선택

- `N과 M (1)`에서 중심이 된 판단은 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`backtracking-concept.md`](../docs/concepts/backtracking-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
