# Problem: 상근이의 여행 (BOJ 9372)

## Problem Statement

$N$개 국가, $M$개 비행기 노선(양방향). 모든 국가를 여행하기 위해 탑승해야 하는 최소 비행기 수를 구하라.

그래프가 연결되어 있음이 보장된다.

## Input

- Line 1: $T$ (테스트 케이스 수)
- 각 테스트 케이스:
  - Line 1: $N$, $M$ ($2 \le N \le 1\,000$, $1 \le M \le 10\,000$)
  - Next $M$ lines: $a$, $b$ (간선)

## Output

각 테스트 케이스에 대해 최소 비행기 탑승 수.

## Examples

**Input**:
```
2
3 3
1 2
2 3
1 3
5 4
2 1
3 2
4 3
5 4
```

**Output**:
```
2
4
```

## Source

https://www.acmicpc.net/problem/9372
