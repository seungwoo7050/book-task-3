# Problem: AC (BOJ 5430)

## Problem Statement

AC is a language with two functions:
- **R**: Reverse the array.
- **D**: Delete the first element. If the array is empty, produce an error.

Given a function string $p$ and an array, execute all functions and print the result. If any D operates on an empty array, print `error`.

## Input

- Line 1: $T$ test cases.
- For each test case:
  - Line 1: Function string $p$ (e.g., `RDD`)
  - Line 2: Number of elements $n$
  - Line 3: Array in format `[x1,x2,...,xn]`

## Constraints

- $1 \le T \le 100$
- $|p| \le 100{,}000$
- $0 \le n \le 100{,}000$

## Output

For each test case, print the resulting array in the same bracket notation, or `error`.

## Examples

**Input**
```
4
RDD
4
[1,2,3,4]
DD
1
[42]
RRD
6
[1,1,2,3,5,8]
D
0
[]
```

**Output**
```
[2,1]
error
[1,2,3,5,8]
error
```

## Source

https://www.acmicpc.net/problem/5430
