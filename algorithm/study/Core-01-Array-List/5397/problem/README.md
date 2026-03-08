# Problem: Keylogger (BOJ 5397)

## Problem Statement

A keylogger has captured a sequence of keystrokes. The keystrokes include:

| Key | Effect |
| :--- | :--- |
| `<` | Move cursor left (ignored if at start) |
| `>` | Move cursor right (ignored if at end) |
| `-` | Delete character to the left of cursor (backspace; ignored if at start) |
| other | Insert character at cursor position |

Given $T$ test cases, output the resulting password for each.

## Input

- Line 1: Integer $T$ ($1 \le T \le 1{,}000$)
- Next $T$ lines: A string of keystrokes (length $\le 1{,}000{,}000$)

The total length of all keystrokes across test cases does not exceed $5{,}000{,}000$.

## Output

For each test case, print the resulting password on a separate line.

## Examples

### Example 1

**Input**
```
2
<<BP<A>>Cd-
ThIsIsS3662
```

**Output**
```
BAPC
ThIsIsS3662
```

## Source

https://www.acmicpc.net/problem/5397
