# Problem: 최단경로 (BOJ 1753)

## Problem Statement

방향 그래프에서 주어진 시작점으로부터 다른 모든 정점까지의 최단 경로를 구하라.

## Input

- Line 1: $V$, $E$ ($1 \le V \le 20\,000$, $1 \le E \le 300\,000$)
- Line 2: 시작 정점 $K$
- Next $E$ lines: $u$, $v$, $w$ (가중치, $1 \le w \le 10$)

## Output

$V$개 줄에 걸쳐 $i$번째 줄에 시작점에서 $i$번 정점까지의 최단 경로값 출력. 경로가 없으면 `INF`.

## Examples

**Input**:
```
5 6
1
5 1 1
1 2 2
1 3 3
2 3 4
2 4 5
3 4 6
```

**Output**:
```
0
2
3
7
INF
```

## Source

https://www.acmicpc.net/problem/1753
