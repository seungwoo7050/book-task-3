# Problem: Algorithm Class — DFS 1 (BOJ 24479)

## Problem Statement

Given an undirected graph with $N$ vertices and $M$ edges, perform DFS starting from vertex $R$. When choosing which neighbor to visit next, always pick the one with the **smallest** number first. For each vertex, output which order it was visited in ($0$ if never visited).

## Input

- Line 1: $N$, $M$, $R$ ($1 \le N \le 100{,}000$; $1 \le M \le 200{,}000$; $1 \le R \le N$)
- Next $M$ lines: Two integers $u$, $v$ — an edge between $u$ and $v$

## Output

$N$ lines: the $i$-th line is the visit order of vertex $i$ ($0$ if unvisited).

## Examples

**Input**
```
5 5 1
1 4
1 2
2 3
2 4
3 4
```

**Output**
```
1
2
3
4
0
```

## Source

https://www.acmicpc.net/problem/24479
