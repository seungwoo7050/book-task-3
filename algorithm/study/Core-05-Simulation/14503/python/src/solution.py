import sys
input = sys.stdin.readline

def main():
    N, M = map(int, input().split())
    r, c, d = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]

    # Direction: 0=N, 1=E, 2=S, 3=W
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    cleaned = [[False] * M for _ in range(N)]
    count = 0

    while True:
        # Step 1: Clean current cell
        if not cleaned[r][c]:
            cleaned[r][c] = True
            count += 1

        # Step 2: Try turning left 4 times
        found = False
        for _ in range(4):
            d = (d + 3) % 4  # turn left
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < N and 0 <= nc < M and grid[nr][nc] == 0 and not cleaned[nr][nc]:
                r, c = nr, nc
                found = True
                break

        if found:
            continue

        # Step 3: All four directions blocked — try moving backward
        bd = (d + 2) % 4  # opposite direction
        br, bc = r + dr[bd], c + dc[bd]
        if 0 <= br < N and 0 <= bc < M and grid[br][bc] != 1:
            r, c = br, bc
        else:
            break  # wall behind — stop

    print(count)

if __name__ == "__main__":
    main()
