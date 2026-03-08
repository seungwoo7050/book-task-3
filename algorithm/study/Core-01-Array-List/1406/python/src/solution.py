import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    m = int(input())

    # Two-stack model: left = chars before cursor, right = chars after cursor (reversed)
    left = list(s)
    right = []

    for _ in range(m):
        cmd = input().strip()
        if cmd == 'L':
            if left:
                right.append(left.pop())
        elif cmd == 'D':
            if right:
                left.append(right.pop())
        elif cmd == 'B':
            if left:
                left.pop()
        elif cmd[0] == 'P':
            left.append(cmd[2])

    # Final string: left (bottom→top) + right (top→bottom)
    print(''.join(left) + ''.join(reversed(right)))

if __name__ == "__main__":
    solve()
