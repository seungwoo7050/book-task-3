# Problem: Install Routers (BOJ 2110)

## Problem Statement

There are $N$ houses on a number line. Install $C$ routers in $C$ distinct houses such that the **minimum distance** between any two routers is **maximized**. Print that maximum possible minimum distance.

## Input

- Line 1: $N$, $C$ ($2 \le C \le N \le 200\,000$)
- Next $N$ lines: one integer each — position of each house ($0 \le x \le 1\,000\,000\,000$)

## Output

Print the maximum possible minimum distance.

## Examples

**Input**:
```
5 3
1
2
8
4
9
```

**Output**: `3`

(Install at houses 1, 4, 8 → distances 3, 4 → min is 3.)

## Source

https://www.acmicpc.net/problem/2110
