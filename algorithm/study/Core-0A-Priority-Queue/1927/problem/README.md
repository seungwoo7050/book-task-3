# Problem: Min Heap (BOJ 1927)

## Problem Statement

Implement a min-heap supporting two operations:
- **Insert** a natural number $x$.
- **Extract** and print the minimum value (print 0 if the heap is empty).

## Input

- Line 1: $N$ ($1 \le N \le 100\,000$)
- Next $N$ lines: an integer $x$. If $x > 0$, insert $x$. If $x = 0$, extract min.

## Output

For each extract operation, print the minimum (or 0 if empty), one per line.

## Examples

**Input**:
```
9
0
12345678
1
2
0
0
0
0
0
```

**Output**:
```
0
1
2
12345678
0
0
```

## Source

https://www.acmicpc.net/problem/1927
