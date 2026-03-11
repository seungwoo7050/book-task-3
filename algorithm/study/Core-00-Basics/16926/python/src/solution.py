import sys
input = sys.stdin.readline

def solve():
    N, M, R = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    layers = min(N, M) // 2

    for k in range(layers):
        # k번째 레이어를 1차원 리스트로 펼친다(시계 방향 순회)
        ring = []
        # 윗줄: left에서 right까지
        for j in range(k, M - k):
            ring.append(arr[k][j])
        # 오른쪽 열: top+1에서 bottom까지
        for i in range(k + 1, N - k):
            ring.append(arr[i][M - 1 - k])
        # 아랫줄: right-1에서 left까지
        for j in range(M - 2 - k, k - 1, -1):
            ring.append(arr[N - 1 - k][j])
        # 왼쪽 열: bottom-1에서 top+1까지
        for i in range(N - 2 - k, k, -1):
            ring.append(arr[i][k])

        # R번 반시계 회전한다(리스트를 왼쪽으로 R칸 이동)
        L = len(ring)
        r = R % L
        ring = ring[r:] + ring[:r]

        # 배열에 다시 써 넣는다
        idx = 0
        for j in range(k, M - k):
            arr[k][j] = ring[idx]; idx += 1
        for i in range(k + 1, N - k):
            arr[i][M - 1 - k] = ring[idx]; idx += 1
        for j in range(M - 2 - k, k - 1, -1):
            arr[N - 1 - k][j] = ring[idx]; idx += 1
        for i in range(N - 2 - k, k, -1):
            arr[i][k] = ring[idx]; idx += 1

    # 출력
    for row in arr:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    solve()
