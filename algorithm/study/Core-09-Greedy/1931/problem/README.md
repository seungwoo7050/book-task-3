# Problem: Meeting Room Assignment (BOJ 1931)

## Problem Statement

Given $N$ meetings, each with a start time and end time, find the maximum number of non-overlapping meetings that can be scheduled in one room. A meeting that ends at time $t$ can be immediately followed by one that starts at time $t$.

## Input

- Line 1: $N$ ($1 \le N \le 100\,000$)
- Next $N$ lines: start and end times ($0 \le start \le end \le 2^{31} - 1$)

## Output

Print the maximum number of meetings.

## Examples

**Input**:
```
11
1 4
3 5
0 6
5 7
3 8
5 9
6 10
8 11
8 12
2 13
12 14
```

**Output**: `4`

## Source

https://www.acmicpc.net/problem/1931
