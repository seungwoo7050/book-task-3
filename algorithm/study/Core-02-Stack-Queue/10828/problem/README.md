# Problem: Stack (BOJ 10828)

## Problem Statement

Implement a stack that supports the following commands:

| Command | Effect |
| :--- | :--- |
| `push X` | Push integer $X$ onto the stack |
| `pop` | Pop and print the top element ($-1$ if empty) |
| `size` | Print the number of elements |
| `empty` | Print $1$ if empty, $0$ otherwise |
| `top` | Print the top element ($-1$ if empty) |

## Input

- Line 1: Integer $N$ ($1 \le N \le 10{,}000$)
- Next $N$ lines: One command each

## Output

For each command that produces output, print the result on a separate line.

## Examples

### Example 1

**Input**
```
14
push 1
push 2
top
size
empty
pop
pop
pop
size
empty
pop
push 3
empty
top
```

**Output**
```
2
2
0
2
1
-1
0
1
-1
0
3
```

## Source

https://www.acmicpc.net/problem/10828
