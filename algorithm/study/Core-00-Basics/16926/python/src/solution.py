import sys
input = sys.stdin.readline

def solve():
    N, M, R = map(int, input().split())
    arr = [list(map(int, input().split())) for _ in range(N)]

    layers = min(N, M) // 2

    for k in range(layers):
        # Extract layer k into a 1D list (clockwise traversal)
        ring = []
        # Top row: left to right
        for j in range(k, M - k):
            ring.append(arr[k][j])
        # Right column: top+1 to bottom
        for i in range(k + 1, N - k):
            ring.append(arr[i][M - 1 - k])
        # Bottom row: right-1 to left
        for j in range(M - 2 - k, k - 1, -1):
            ring.append(arr[N - 1 - k][j])
        # Left column: bottom-1 to top+1
        for i in range(N - 2 - k, k, -1):
            ring.append(arr[i][k])

        # Rotate counterclockwise by R (= shift list left by R)
        L = len(ring)
        r = R % L
        ring = ring[r:] + ring[:r]

        # Write back to the array
        idx = 0
        for j in range(k, M - k):
            arr[k][j] = ring[idx]; idx += 1
        for i in range(k + 1, N - k):
            arr[i][M - 1 - k] = ring[idx]; idx += 1
        for j in range(M - 2 - k, k - 1, -1):
            arr[N - 1 - k][j] = ring[idx]; idx += 1
        for i in range(N - 2 - k, k, -1):
            arr[i][k] = ring[idx]; idx += 1

    # Output
    for row in arr:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    solve()
