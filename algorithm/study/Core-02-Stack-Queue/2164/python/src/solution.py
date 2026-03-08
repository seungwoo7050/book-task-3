import sys
from collections import deque

def solve():
    n = int(sys.stdin.readline())
    q = deque(range(1, n + 1))

    while len(q) > 1:
        q.popleft()          # discard top card
        q.append(q.popleft()) # move next card to bottom

    print(q[0])

if __name__ == "__main__":
    solve()
