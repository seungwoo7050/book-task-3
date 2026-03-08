# Problem: Array Rotation 1 (BOJ 16926)

## Problem Statement

Given an $N \times M$ array and an integer $R$, rotate the array counterclockwise by $R$ steps and print the result.

The array is composed of $\min(N, M) / 2$ concentric rectangular layers. Each layer is rotated independently.

## Input

- Line 1: Three integers $N$, $M$, $R$ separated by spaces.
- Lines 2 to $N+1$: $M$ integers per line representing the array.

### Constraints

- $2 \le N, M \le 300$
- $1 \le R \le 10^9$
- $\min(N, M) \mod 2 = 0$
- $1 \le A_{i,j} \le 10^8$

## Output

Print the rotated $N \times M$ array, with elements separated by spaces.

## Examples

### Example 1

**Input**
```
4 4 2
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
```

**Output**
```
3 4 8 12
2 11 10 16
1 7 6 15
5 9 13 14
```

### Example 2

**Input**
4 4 1
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 16
```

**Output**
```
2 3 4 8
1 7 11 12
5 6 10 16
9 13 14 15
```

## Source

https://www.acmicpc.net/problem/16926
