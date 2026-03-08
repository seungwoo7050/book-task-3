# Problem: Editor (BOJ 1406)

## Problem Statement

You have an initial string and a cursor positioned at the **end** of the string. Process $M$ commands:

| Command | Effect |
| :--- | :--- |
| `L` | Move cursor one position left (ignored if at the start) |
| `D` | Move cursor one position right (ignored if at the end) |
| `B` | Delete the character to the left of the cursor (ignored if at the start) |
| `P x` | Insert character `x` to the left of the cursor |

Print the resulting string after all commands.

## Input

- Line 1: Initial string (lowercase letters, length $\le 100{,}000$)
- Line 2: Integer $M$ ($1 \le M \le 500{,}000$)
- Next $M$ lines: One command each

## Output

Print the final string.

## Examples

### Example 1

**Input**
```
abcd
3
P x
L
L
```

**Output**
```
abcdx
```

### Example 2

**Input**
```
abc
9
L
L
L
L
L
P x
L
B
P y
```

**Output**
```
yxbc
```

## Source

https://www.acmicpc.net/problem/1406
