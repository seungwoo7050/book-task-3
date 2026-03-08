# Problem: 줄 세우기 (BOJ 2252)

## Problem Statement

$N$명 학생의 키를 비교한 결과 $M$개가 주어진다. 각 비교는 "학생 $A$가 학생 $B$보다 앞에 서야 한다"를 의미한다. 학생들을 줄 세운 결과를 출력하라.

답이 여러 개일 수 있으며, 아무거나 하나 출력하면 된다.

## Input

- Line 1: $N$, $M$ ($1 \le N \le 32\,000$, $1 \le M \le 100\,000$)
- Next $M$ lines: $A$, $B$ ($A$가 $B$ 앞에 서야 함)

## Output

한 줄에 학생들을 앞에서부터 순서대로 출력.

## Examples

**Input**:
```
3 2
1 3
2 3
```

**Output**:
```
1 2 3
```

## Source

https://www.acmicpc.net/problem/2252
