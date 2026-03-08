# Problem: DFS and BFS (BOJ 1260)

## Problem Statement

Given an undirected graph with $N$ vertices and $M$ edges, starting from vertex $V$:
1. Print the DFS visit order.
2. Print the BFS visit order.

When multiple vertices can be visited, choose the **smaller-numbered** vertex first.

## Input

- Line 1: $N$, $M$, $V$ ($1 \le N \le 1{,}000$; $1 \le M \le 10{,}000$)
- Next $M$ lines: edge endpoints

## Output

- Line 1: DFS order (space-separated)
- Line 2: BFS order (space-separated)

## Examples

**Input**
```
4 5 1
1 2
1 3
1 4
2 4
3 4
```

**Output**
```
1 2 4 3
1 2 3 4
```

## Source

https://www.acmicpc.net/problem/1260
