# BOJ 10872 — 접근 과정: 수학적 정의를 코드로

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
