# 큐(Queue) 개념 정리 — Card2

## 정의

**큐(Queue)**는 FIFO(First-In, First-Out) 원칙을 따르는 선형 자료구조이다.
가장 먼저 삽입된 원소가 가장 먼저 제거된다.

## CLRS 연결

CLRS Ch 10.1 (pp. 234–235)에서 순환 배열 기반 큐를 다음과 같이 정의한다:

```
ENQUEUE(Q, x)
  Q[Q.tail] = x
  if Q.tail == Q.length
    Q.tail = 1
  else Q.tail = Q.tail + 1

DEQUEUE(Q)
  x = Q[Q.head]
  if Q.head == Q.length
    Q.head = 1
  else Q.head = Q.head + 1
  return x
```

- `Q.head`: 가장 오래된 원소의 인덱스
- `Q.tail`: 다음 삽입 위치
- 순환 배열로 공간 재활용

## 카드2 문제에서의 큐 활용

카드 더미를 큐로 모델링:
- **front** = 맨 위 카드
- **back** = 맨 아래 카드

각 라운드:
1. `dequeue()` → 버림 (맨 위 카드 제거)
2. `x = dequeue()` → `enqueue(x)` → 다음 카드를 맨 아래로 이동

$N-1$ 라운드 후 큐에 남은 유일한 원소가 정답이다.

## 자료구조 선택의 중요성

| 구현 | dequeue 시간 | 전체 시간 |
|------|-------------|-----------|
| Python `list.pop(0)` | $O(N)$ | $O(N^2)$ |
| Python `deque.popleft()` | $O(1)$ | $O(N)$ |
| C++ `std::queue` | $O(1)$ | $O(N)$ |

$N = 500{,}000$일 때 $O(N^2) \approx 2.5 \times 10^{11}$으로 TLE.
`deque` 사용은 선택이 아닌 필수이다.

## 수학적 관찰

$N$이 2의 거듭제곱일 때 답은 항상 $N$ 자체이다.
일반적으로 $N = 2^m + l$ ($0 \le l < 2^m$)이면 답은 $2l$이다.
이를 이용하면 $O(1)$에도 풀 수 있지만, 큐 시뮬레이션이 직관적이다.
