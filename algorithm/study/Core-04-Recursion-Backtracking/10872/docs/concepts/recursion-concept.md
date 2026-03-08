# 재귀(Recursion) 개념 정리 — 팩토리얼

## 정의

**재귀(Recursion)**란 함수가 자기 자신을 호출하는 프로그래밍 기법이다.
모든 재귀 함수는 두 가지 요소로 구성된다:

1. **기저 조건(Base Case)**: 재귀를 멈추는 조건
2. **재귀 단계(Recursive Step)**: 자기 자신을 호출하여 문제를 축소

## 팩토리얼의 재귀적 정의

$$n! = \begin{cases} 1 & \text{if } n = 0 \\ n \times (n-1)! & \text{if } n \ge 1 \end{cases}$$

## CLRS 연결 (Ch 4)

CLRS Ch 4는 분할 정복(Divide and Conquer)을 소개한다.
팩토리얼은 분할 정복의 퇴화(degenerate) 형태이다:
- 부분 문제가 **하나**뿐 (크기 $n-1$)
- 결합 단계: 곱셈 $O(1)$

### 점화식과 마스터 정리
$$T(n) = T(n-1) + \Theta(1) = \Theta(n)$$

마스터 정리는 $T(n) = aT(n/b) + f(n)$ 형태에만 적용되므로,
팩토리얼의 선형 점화식은 단순 전개로 $\Theta(n)$을 증명한다.

## 재귀 vs 반복

| 항목 | 재귀 | 반복 |
|------|------|------|
| 코드 | 수학 정의와 1:1 | 루프 변수 필요 |
| 공간 | $O(N)$ (스택) | $O(1)$ |
| 성능 | 함수 호출 오버헤드 | 더 빠름 |
| 가독성 | 수학적 직관 | 절차적 |

```python
# 재귀
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

# 반복
def factorial_iter(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

## 꼬리 재귀(Tail Recursion)

```python
def factorial_tail(n, acc=1):
    if n <= 1: return acc
    return factorial_tail(n - 1, n * acc)
```

일부 언어(Scheme, Scala)는 꼬리 재귀를 자동 최적화한다.
Python은 TCO를 지원하지 않으므로 스택 깊이 제한이 동일.
