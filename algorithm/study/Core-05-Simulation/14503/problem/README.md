# Problem: Robot Vacuum Cleaner (BOJ 14503)

## Problem Statement

A room is an $N \times M$ grid. Each cell is either empty (0) or a wall (1). A robot starts at position $(r, c)$ facing direction $d$ (0=North, 1=East, 2=South, 3=West).

The robot operates as follows:

1. Clean the current cell.
2. Starting from the direction to the left of the current direction, check the four directions in counter-clockwise order:
   a. If the cell in that direction is uncleaned empty space, move forward one step in that direction and turn to face that direction. Go to step 1.
   b. If all four directions are either walls or already cleaned:
      - If the cell **behind** the robot (opposite of current facing) is empty (wall or cleaned doesn't matter, as long as it's not a wall), move backward one step without changing direction. Go to step 2.
      - If the cell behind is a wall, stop.

Print the number of cells the robot cleans.

## Input

- Line 1: $N$ $M$ ($3 \le N, M \le 50$)
- Line 2: $r$ $c$ $d$
- Next $N$ lines: $M$ integers (0 or 1)

## Output

Print the number of cells cleaned.

## Examples

**Input**:
```
3 3
1 1 0
1 1 1
1 0 1
1 1 1
```

**Output**: `1`

**Input**:
```
11 10
7 4 0
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1
1 0 0 0 1 1 1 1 0 1
1 0 0 1 1 0 0 0 0 1
1 0 1 1 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 1 0 1
1 0 0 0 0 0 1 1 0 1
1 0 0 0 0 0 1 1 0 1
1 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1
```

**Output**: `57`

## Source

https://www.acmicpc.net/problem/14503
