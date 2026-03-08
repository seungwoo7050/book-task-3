# Problem: Gear (BOJ 14891)

## Problem Statement

There are 4 gears, each with 8 teeth arranged in a circle. Each tooth is either N-pole (0) or S-pole (1). The teeth are numbered 0–7 clockwise starting from the 12 o'clock position. The right contact point of a gear is tooth index 2, and the left contact point is tooth index 6.

Given $K$ rotation commands, each specifying a gear number and direction (1 = clockwise, −1 = counter-clockwise):

1. Before rotating, check adjacent gears. If two adjacent gears have **different** poles at their contact points, the adjacent gear rotates in the **opposite** direction; if the poles are the **same**, it does not rotate.
2. Propagation ripples outward (gear 1↔2, 2↔3, 3↔4).
3. After all rotations are determined, rotate all affected gears simultaneously.

After processing all commands, compute the score:
- Gear 1 top (index 0) is S-pole → +1
- Gear 2 top (index 0) is S-pole → +2
- Gear 3 top (index 0) is S-pole → +4
- Gear 4 top (index 0) is S-pole → +8

Print the total score.

## Input

- Lines 1–4: 8-character string of `0`s and `1`s for each gear.
- Line 5: integer $K$ ($1 \le K \le 100$).
- Next $K$ lines: two integers — gear number (1–4) and direction (1 or −1).

## Output

Print the total score.

## Examples

**Input**:
```
10101111
01111101
11001110
00000010
2
3 -1
1 1
```

**Output**: `7`

## Source

https://www.acmicpc.net/problem/14891
