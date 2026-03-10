# 접근 로그

> 프로젝트: 팩토리얼
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 재귀 구현

수학적 정의를 그대로 번역했다:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

기저 조건: $n \leq 1$이면 1 반환. $0! = 1$과 $1! = 1$을 모두 처리한다.

## 대안 검토

1. **반복문**: `result = 1; for i in range(2, n+1): result *= i` — 스택 오버플로우 걱정 없음
2. **math.factorial**: 내장 함수 — 한 줄이면 끝나지만 학습 목적에 맞지 않음
3. **꼬리 재귀**: Python은 꼬리 재귀 최적화를 지원하지 않으므로 의미 없음

재귀 연습이 목적이므로 재귀 구현을 선택했다.

## 입력 처리

`sys.stdin.readline()`으로 단일 정수를 읽는다. 이 문제에서는 I/O 최적화가 의미 없지만(입력 1개), 다른 문제들과의 일관성을 위해 동일한 패턴을 사용한다.

## 호출 스택 추적

$N = 4$ 예시:
```
factorial(4) → 4 * factorial(3)
  factorial(3) → 3 * factorial(2)
    factorial(2) → 2 * factorial(1)
      factorial(1) → 1  (기저 조건)
    → 2 * 1 = 2
  → 3 * 2 = 6
→ 4 * 6 = 24
```

이 스택 추적이 15649의 백트래킹에서 "선택 → 재귀 → 되돌림" 패턴으로 확장된다.

## 이 접근에서 꼭 기억할 선택

- `팩토리얼`에서 중심이 된 판단은 `호출 구조를 추적하고 상태 복원 규칙을 설명하는 연습`를 가장 단순한 상태 전이로 번역하는 것이었다.
- 대안이 더 화려해 보여도, 자동 검증과 설명 가능성을 함께 만족하는 쪽이 학습 레포에서는 더 가치가 있다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 구현 이유를 따라가다가 막히면 `05-development-timeline.md`로 돌아가 실제로 어떤 순서로 판단을 굳혔는지 다시 보는 편이 좋다.

## 다음에 다시 풀 때의 질문

- 같은 문제를 더 작은 자료구조나 더 적은 상태로 설명할 수 있는가?
- 지금 선택한 전략이 경계 사례에서도 동일하게 유지되는가?
- 코드보다 먼저 적어 둘 한 문장은 무엇인가?

## 같이 읽을 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`recursion-concept.md`](../docs/concepts/recursion-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- [`05-development-timeline.md`](05-development-timeline.md)
