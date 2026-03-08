# Problem: Coin 0 (BOJ 11047)

## Problem Statement

Given $N$ coin denominations (in ascending order, each divides the next) and a target amount $K$, find the minimum number of coins to make exactly $K$.

## Input

- Line 1: $N$, $K$ ($1 \le N \le 10$, $1 \le K \le 100\,000\,000$)
- Next $N$ lines: one coin value each (ascending, $A_1 = 1$, $A_i | A_{i+1}$)

## Output

Print the minimum number of coins.

## Examples

**Input**:
```
10 4200
1
5
10
50
100
500
1000
5000
10000
50000
```

**Output**: `6`

## Source

https://www.acmicpc.net/problem/11047
