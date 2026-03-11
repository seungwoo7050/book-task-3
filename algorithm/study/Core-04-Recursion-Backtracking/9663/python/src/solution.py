import sys

def solve():
    n = int(sys.stdin.readline())
    col = [False] * n
    diag1 = [False] * (2 * n)  # 부대각선 인덱스(row - col + n - 1)
    diag2 = [False] * (2 * n)  # 주대각선 인덱스(row + col)
    count = 0

    def place(row):
        nonlocal count
        if row == n:
            count += 1
            return
        for c in range(n):
            if not col[c] and not diag1[row - c + n - 1] and not diag2[row + c]:
                col[c] = diag1[row - c + n - 1] = diag2[row + c] = True
                place(row + 1)
                col[c] = diag1[row - c + n - 1] = diag2[row + c] = False

    place(0)
    print(count)

if __name__ == "__main__":
    solve()
