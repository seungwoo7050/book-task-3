import sys
from collections import deque
input = sys.stdin.readline

def solve():
    M, N = map(int, input().split())
    grid = []
    q = deque()

    for i in range(N):
        row = list(map(int, input().split()))
        grid.append(row)
        for j in range(M):
            if row[j] == 1:
                q.append((i, j, 0))  # row, col, day

    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]
    ans = 0

    while q:
        x, y, day = q.popleft()
        for k in range(4):
            nx, ny = x + dx[k], y + dy[k]
            if 0 <= nx < N and 0 <= ny < M and grid[nx][ny] == 0:
                grid[nx][ny] = 1
                q.append((nx, ny, day + 1))
                ans = max(ans, day + 1)

    # Check if any unripe tomato remains
    for row in grid:
        if 0 in row:
            print(-1)
            return

    print(ans)

if __name__ == "__main__":
    solve()
