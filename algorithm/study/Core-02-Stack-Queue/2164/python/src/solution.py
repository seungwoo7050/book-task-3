import sys
from collections import deque

def solve():
    n = int(sys.stdin.readline())
    q = deque(range(1, n + 1))

    while len(q) > 1:
        q.popleft()          # 맨 위 카드를 버린다
        q.append(q.popleft()) # 다음 카드를 맨 아래로 보낸다

    print(q[0])

if __name__ == "__main__":
    solve()
