# Problem: Card Sorting (BOJ 1715)

## Problem Statement

$N$ 개의 카드 묶음이 있다. 두 묶음을 합칠 때 비교 횟수는 두 묶음 크기의 합이다. 모든 묶음을 하나로 합칠 때 필요한 최소 비교 횟수를 구하라.

## Input

- Line 1: $N$ ($1 \le N \le 100\,000$)
- Next $N$ lines: 각 묶음의 카드 수 ($\le 1\,000$)

## Output

최소 비교 횟수를 출력한다.

## Examples

### Example 1

**Input**:
```
3
10
20
40
```

**Output**:
```
100
```

**Explanation**: 10+20=30 (비용 30), 30+40=70 (비용 70) → 총 100.

## Source

https://www.acmicpc.net/problem/1715
