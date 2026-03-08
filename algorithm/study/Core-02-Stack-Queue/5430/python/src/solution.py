import sys
from collections import deque

def solve():
    t = int(sys.stdin.readline())
    for _ in range(t):
        p = sys.stdin.readline().strip()
        n = int(sys.stdin.readline())
        arr_str = sys.stdin.readline().strip()

        # Parse array from "[x1,x2,...,xn]"
        if n == 0:
            dq = deque()
        else:
            dq = deque(arr_str[1:-1].split(','))

        is_reversed = False
        error = False

        for cmd in p:
            if cmd == 'R':
                is_reversed = not is_reversed
            elif cmd == 'D':
                if not dq:
                    error = True
                    break
                if is_reversed:
                    dq.pop()
                else:
                    dq.popleft()

        if error:
            print("error")
        else:
            if is_reversed:
                dq.reverse()
            print('[' + ','.join(dq) + ']')

if __name__ == "__main__":
    solve()
