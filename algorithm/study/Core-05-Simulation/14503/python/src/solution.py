import sys
input = sys.stdin.readline

def main():
    N, M = map(int, input().split())
    r, c, d = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]

    # 방향 인코딩: 0=N, 1=E, 2=S, 3=W
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    cleaned = [[False] * M for _ in range(N)]
    count = 0

    while True:
        # 1단계: 현재 칸을 청소
        if not cleaned[r][c]:
            cleaned[r][c] = True
            count += 1

        # 2단계: 왼쪽 회전을 최대 4번 시도
        found = False
        for _ in range(4):
            d = (d + 3) % 4  # 왼쪽으로 회전
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < N and 0 <= nc < M and grid[nr][nc] == 0 and not cleaned[nr][nc]:
                r, c = nr, nc
                found = True
                break

        if found:
            continue

        # 3단계: 네 방향이 모두 막히면 뒤로 이동을 시도
        bd = (d + 2) % 4  # 반대 방향
        br, bc = r + dr[bd], c + dc[bd]
        if 0 <= br < N and 0 <= bc < M and grid[br][bc] != 1:
            r, c = br, bc
        else:
            break  # 뒤가 벽이면 종료

    print(count)

if __name__ == "__main__":
    main()
