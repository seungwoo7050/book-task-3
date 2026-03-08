# Problem: Tomato (BOJ 7576)

## Problem Statement

A warehouse contains tomatoes in an $N \times M$ grid:
- `1`: ripe tomato
- `0`: unripe tomato
- `-1`: empty cell

Each day, a ripe tomato ripens adjacent (up/down/left/right) unripe tomatoes. Find the minimum number of days until all tomatoes are ripe. If some tomatoes can never ripen, print `-1`. If all are already ripe, print `0`.

## Input

- Line 1: $M$, $N$ ($2 \le M, N \le 1{,}000$)
- Next $N$ lines: $M$ integers per line

## Output

Print the minimum number of days, or `-1`.

## Examples

**Input**
```
6 4
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 1
```

**Output**
```
8
```

## Source

https://www.acmicpc.net/problem/7576
