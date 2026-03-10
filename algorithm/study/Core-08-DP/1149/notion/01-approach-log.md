# 접근 로그

> 프로젝트: RGB거리
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 상태 정의

$\textrm{dp}[i][c]$ = $i$번 집까지 칠했을 때, $i$번 집의 색이 $c$일 때의 최소 비용

## 점화식

$$\textrm{dp}[i][c] = \textrm{cost}[i][c] + \min(\textrm{dp}[i-1][c'] \mid c' \neq c)$$

즉, 현재 집을 색 $c$로 칠하려면, 이전 집은 $c$가 아닌 나머지 두 색 중 최소 비용인 것을 선택.

## 공간 최적화

$\textrm{dp}[i]$는 $\textrm{dp}[i-1]$에만 의존하므로, 2D 배열 대신 **이전 행 변수 3개**만 유지:

```python
prev = list(map(int, input().split()))  # 첫 번째 집
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

$O(N)$ 시간, $O(1)$ 공간 (상수 3개).

## 왜 그리디가 안 되는가

"매 집에서 가장 싼 색을 선택"하면 인접 제약을 만족하지 못하거나, 전체 최소를 놓칠 수 있다. DP가 필요한 이유.

## 이 접근에서 꼭 기억할 선택

- `RGB거리`에서 중심이 된 판단은 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`dp-rgb-concept.md`](../docs/concepts/dp-rgb-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
