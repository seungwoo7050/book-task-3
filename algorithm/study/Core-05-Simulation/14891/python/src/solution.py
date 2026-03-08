import sys
from collections import deque
input = sys.stdin.readline

def main():
    # Read 4 gears (each as a deque of ints)
    gears = [deque(int(c) for c in input().strip()) for _ in range(4)]

    K = int(input())
    for _ in range(K):
        num, d = map(int, input().split())
        num -= 1  # 0-indexed

        # Determine rotation direction for each gear
        dirs = [0] * 4
        dirs[num] = d

        # Propagate left
        for i in range(num - 1, -1, -1):
            if gears[i][2] != gears[i + 1][6]:
                dirs[i] = -dirs[i + 1]
            else:
                break  # no further propagation

        # Propagate right
        for i in range(num + 1, 4):
            if gears[i][6] != gears[i - 1][2]:
                dirs[i] = -dirs[i - 1]
            else:
                break

        # Apply rotations
        for i in range(4):
            if dirs[i] == 1:        # clockwise
                gears[i].appendleft(gears[i].pop())
            elif dirs[i] == -1:     # counter-clockwise
                gears[i].append(gears[i].popleft())

    # Compute score
    score = sum(gears[i][0] * (1 << i) for i in range(4))
    print(score)

if __name__ == "__main__":
    main()
