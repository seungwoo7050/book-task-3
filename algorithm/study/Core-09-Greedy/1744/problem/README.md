# Problem: Number Bundling (BOJ 1744)

## Problem Statement

Given $N$ integers, you can pair some of them (each number used at most once). Paired numbers contribute their **product** to the sum; unpaired numbers contribute their value. Maximize the total sum.

## Input

- Line 1: $N$ ($1 \le N \le 50$)
- Next $N$ lines: one integer each ($-1000 \le a_i \le 1000$)

## Output

Print the maximum sum.

## Examples

**Input**:
```
4
-1
2
1
3
```

**Output**: `6`

(Pair (2,3)→6, keep (-1) and (1) unpaired → 6 + (-1) + 1 = 6)

## Source

https://www.acmicpc.net/problem/1744
