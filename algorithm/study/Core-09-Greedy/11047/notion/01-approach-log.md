# 접근 로그

> 프로젝트: 동전 0
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 핵심 관찰

동전이 배수 관계 → 큰 동전을 최대한 쓰는 것이 항상 최적.

## 알고리즘

```python
for coin in reversed(coins):
    count += K // coin
    K %= coin
```

1. 가장 큰 동전부터 순회
2. 해당 동전으로 만들 수 있는 최대 개수 = `K // coin`
3. 나머지 = `K %= coin`

## 그리디 정당성

배수 조건: $A_i | A_{i+1}$. 따라서 큰 동전 1개 = 작은 동전 여러 개와 정확히 교환 가능. 큰 동전 1개를 쓰지 않으면 같은 금액을 더 많은 작은 동전으로 채워야 하므로, 큰 것부터 쓰는 것이 항상 최적.

## 반례가 되는 경우

배수 조건이 없다면 (예: 1, 3, 4로 6 만들기), 그리디는 4+1+1=3개, 최적은 3+3=2개. 이 경우 DP가 필요.

## 시간/공간
- $O(N)$

## 이 접근에서 꼭 기억할 선택

- `동전 0`에서 중심이 된 판단은 `탐욕 선택의 기준을 말로 설명하고 반례 가능성을 점검하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`greedy-coin-concept.md`](../docs/concepts/greedy-coin-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
