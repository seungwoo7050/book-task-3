# Problem: 타임머신 (BOJ 11657)

## Problem Statement

$N$개 도시, $M$개 버스(방향). 일부 노선의 비용이 음수일 수 있다. 1번 도시에서 나머지 도시까지의 최단 시간을 구하라. 음의 사이클이 존재하면 `-1`을 출력한다.

## Input

- Line 1: $N$, $M$ ($1 \le N \le 500$, $1 \le M \le 6\,000$)
- Next $M$ lines: $A$, $B$, $C$ ($-10\,000 \le C \le 10\,000$)

## Output

만약 1번 도시에서 출발하여 음의 사이클로 무한히 줄일 수 있다면 `-1`만 출력.
그렇지 않으면 $N - 1$개 줄에 2번~$N$번 도시까지 최단 시간. 갈 수 없으면 `-1`.

## Examples

**Input**:
```
3 4
1 2 4
1 3 3
2 3 -1
3 1 -2
```

**Output**:
```
4
3
```

## Source

https://www.acmicpc.net/problem/11657
