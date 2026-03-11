import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    m = int(input())

    # 두 스택 모델: left = 커서 왼쪽, right = 커서 오른쪽(역순)
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

    # 최종 문자열: left(아래→위) + right(위→아래)
    print(''.join(left) + ''.join(reversed(right)))

if __name__ == "__main__":
    solve()
