# Problem: Max Heap (BOJ 11279)

## Problem Statement

Implement a max-heap supporting two operations:
- **Insert** a natural number $x$.
- **Extract** and print the maximum value (print 0 if the heap is empty).

## Input

- Line 1: $N$ ($1 \le N \le 100\,000$)
- Next $N$ lines: an integer $x$. If $x > 0$, insert $x$. If $x = 0$, extract max.

## Output

For each extract operation, print the maximum (or 0 if empty), one per line.

## Examples

**Input**:
```
13
0
1
2
0
0
3
2
1
0
0
0
0
0
```

**Output**:
```
0
2
1
3
2
1
0
0
```

## Source

https://www.acmicpc.net/problem/11279
