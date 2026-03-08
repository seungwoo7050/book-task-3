# Problem: Word Sort (BOJ 1181)

## Problem Statement

Given $N$ words consisting of lowercase English letters, sort them according to these rules:

1. Shorter words come first.
2. Among words of equal length, sort lexicographically.
3. Remove duplicates.

## Input

- Line 1: integer $N$ ($1 \le N \le 20000$)
- Next $N$ lines: one word each (length ≤ 50)

## Output

Print the sorted words, one per line, with duplicates removed.

## Examples

**Input**:
```
13
but
i
wont
hesitate
no
more
no
more
it
cannot
wait
im
yours
```

**Output**:
```
i
im
it
no
but
more
wait
wont
yours
cannot
hesitate
```

## Source

https://www.acmicpc.net/problem/1181
