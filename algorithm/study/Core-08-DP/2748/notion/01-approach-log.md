# 접근 로그

> 프로젝트: 피보나치 수 2
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## Bottom-Up 방식 (채택)

배열 대신 변수 두 개로 이전 두 값만 유지:

```python
a, b = 0, 1
for _ in range(2, n + 1):
    a, b = b, a + b
print(b)
```

$O(n)$ 시간, $O(1)$ 공간.

## 대안

1. **재귀 + 메모이제이션**: `@lru_cache`로 top-down DP. $O(n)$ 시간, $O(n)$ 공간.
2. **행렬 거듭제곱**: $[[1,1],[1,0]]^n$으로 $O(\log n)$. 이 문제에서는 과한 설계.
3. **순수 재귀**: $O(2^n)$. $n = 90$에서 사실상 불가능.

## 기저 조건

$n \leq 1$이면 $n$ 자체를 반환. $F(0) = 0, F(1) = 1$.

## 이 접근에서 꼭 기억할 선택

- `피보나치 수 2`에서 중심이 된 판단은 `상태와 전이를 명시적으로 정의하고 표나 배열 의미를 끝까지 유지하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`dp-fib-concept.md`](../docs/concepts/dp-fib-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
