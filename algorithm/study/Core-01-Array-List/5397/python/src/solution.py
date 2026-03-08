import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        keys = input().strip()
        left = []   # characters to the left of cursor
        right = []  # characters to the right of cursor (reversed)

        for ch in keys:
            if ch == '<':
                if left:
                    right.append(left.pop())
            elif ch == '>':
                if right:
                    left.append(right.pop())
            elif ch == '-':
                if left:
                    left.pop()
            else:
                left.append(ch)

        # Combine: left stack + reversed right stack
        sys.stdout.write(''.join(left) + ''.join(reversed(right)) + '\n')

if __name__ == "__main__":
    solve()
