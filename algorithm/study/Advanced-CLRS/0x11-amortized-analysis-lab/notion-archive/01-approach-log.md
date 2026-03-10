# 0x11 Amortized Analysis Lab — 접근 과정

## Stack MULTIPOP

- PUSH: 비용 1
- POP: 비용 1
- MULTIPOP(k): min(k, size)개 pop, 비용 = pop 횟수

총 비용이 $O(n)$임을 보이는 것이 핵심 (각 원소는 최대 한 번 push, 한 번 pop).

## Binary Counter

- INC: value + 1, 비용 = 변경된 비트 수 (XOR의 popcount)

총 비용이 $O(n)$임을 보이는 것이 핵심 (각 비트 위치 $i$는 $n/2^i$번 변경).

## 구현

```python
cost += (value ^ nxt).bit_count()
```

XOR로 변경된 비트 수를 직접 세는 우아한 방법.
