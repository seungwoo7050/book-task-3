# Problem: 트리의 부모 찾기 (BOJ 11725)

## Problem Statement

루트가 1인 트리가 주어질 때, 각 노드의 부모를 구하라.

## Input

- Line 1: $N$ ($2 \le N \le 100\,000$)
- Next $N-1$ lines: 간선을 이루는 두 정점 $u, v$

## Output

2번 노드부터 $N$번 노드까지 각 노드의 부모 노드 번호를 한 줄에 하나씩 출력한다.

## Examples

**Input**:
```
7
1 6
6 3
3 5
4 1
2 4
4 7
```

**Output**:
```
4
6
1
3
1
4
```

## Source

https://www.acmicpc.net/problem/11725
