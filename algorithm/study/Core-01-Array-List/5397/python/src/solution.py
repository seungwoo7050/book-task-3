import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        keys = input().strip()
        left = []   # 커서 왼쪽 문자들
        right = []  # 커서 오른쪽 문자들(역순 보관)

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

        # 합치기: left 스택 + 뒤집힌 right 스택
        sys.stdout.write(''.join(left) + ''.join(reversed(right)) + '\n')

if __name__ == "__main__":
    solve()
