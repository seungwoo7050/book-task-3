import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    stack = []
    out = []

    for _ in range(n):
        cmd = input().split()
        if cmd[0] == 'push':
            stack.append(int(cmd[1]))
        elif cmd[0] == 'pop':
            out.append(str(stack.pop()) if stack else '-1')
        elif cmd[0] == 'size':
            out.append(str(len(stack)))
        elif cmd[0] == 'empty':
            out.append('1' if not stack else '0')
        elif cmd[0] == 'top':
            out.append(str(stack[-1]) if stack else '-1')

    print('\n'.join(out))

if __name__ == "__main__":
    solve()
