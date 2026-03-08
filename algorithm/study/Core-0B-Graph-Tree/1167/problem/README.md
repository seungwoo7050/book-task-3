# Problem: 트리의 지름 (BOJ 1167)

## Problem Statement

트리의 지름이란, 트리에서 임의의 두 정점 사이의 거리 중 가장 긴 것을 말한다. 트리의 지름을 구하라.

## Input

- Line 1: $V$ ($2 \le V \le 100\,000$)
- Next $V$ lines: 정점 번호, 이후 (인접 정점, 가중치) 쌍들, -1로 종료.

## Output

트리의 지름을 출력한다.

## Examples

**Input**:
```
5
1 3 2 -1
2 4 4 -1
3 1 2 4 3 -1
4 2 4 3 3 5 6 -1
5 4 6 -1
```

**Output**:
```
11
```

## Source

https://www.acmicpc.net/problem/1167
