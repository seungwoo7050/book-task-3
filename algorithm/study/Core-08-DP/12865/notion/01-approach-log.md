# 접근 로그

> 프로젝트: 평범한 배낭
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 2D DP 원형

$\textrm{dp}[i][j]$ = 처음 $i$개 물건으로 용량 $j$인 배낭을 채울 때의 최대 가치

점화식:
$$\textrm{dp}[i][j] = \max(\textrm{dp}[i-1][j],\ \textrm{dp}[i-1][j - w_i] + v_i)$$

$O(NK)$ 시간, $O(NK)$ 공간.

## 1D 최적화

$\textrm{dp}[i]$는 $\textrm{dp}[i-1]$에만 의존. 1D 배열로 축소:

```python
dp = [0] * (K + 1)
for _ in range(N):
    w, v = map(int, input().split())
    for j in range(K, w - 1, -1):
        dp[j] = max(dp[j], dp[j - w] + v)
```

**역순 순회가 핵심**: 순방향으로 돌면 같은 아이템을 여러 번 넣는 효과가 생긴다 (이것은 완전 배낭 문제). 역순이면 각 아이템이 한 번만 사용된다.

## 왜 역순인가?

`dp[j - w]`를 참조할 때, 이 값이 "현재 아이템을 아직 고려하지 않은" 상태여야 한다. 역순이면 `j - w < j`이므로 아직 갱신되지 않은 값을 참조한다.

## 시간/공간

- $O(NK)$ 시간, $O(K)$ 공간

## 이 접근에서 꼭 기억할 선택

- `평범한 배낭`에서 중심이 된 판단은 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`knapsack-concept.md`](../docs/concepts/knapsack-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
