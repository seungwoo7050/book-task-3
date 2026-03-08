# Problem: 트리 순회 (BOJ 1991)

## Problem Statement

이진 트리가 주어졌을 때, 전위(preorder), 중위(inorder), 후위(postorder) 순회한 결과를 출력하라.

## Input

- Line 1: $N$ ($1 \le N \le 26$)
- Next $N$ lines: 노드, 왼쪽 자식, 오른쪽 자식 (없으면 `.`)

루트는 항상 `A`이다.

## Output

- Line 1: 전위 순회 결과
- Line 2: 중위 순회 결과
- Line 3: 후위 순회 결과

## Examples

**Input**:
```
7
A B C
B D .
C E F
D . .
E . .
F . G
G . .
```

**Output**:
```
ABDCEFG
DBAECFG
DBEGFCA
```

## Source

https://www.acmicpc.net/problem/1991
