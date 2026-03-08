import sys
input = sys.stdin.readline

def add(a, b):
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]

def sub(a, b):
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]

def naive(a, b):
    n = len(a)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = a[i][k]
            for j in range(n):
                out[i][j] += aik * b[k][j]
    return out

def split(m):
    mid = len(m) // 2
    return (
        [row[:mid] for row in m[:mid]],
        [row[mid:] for row in m[:mid]],
        [row[:mid] for row in m[mid:]],
        [row[mid:] for row in m[mid:]],
    )

def combine(c11, c12, c21, c22):
    top = [x + y for x, y in zip(c11, c12)]
    bottom = [x + y for x, y in zip(c21, c22)]
    return top + bottom

def strassen(a, b):
    n = len(a)
    if n <= 2:
        return naive(a, b)
    a11, a12, a21, a22 = split(a)
    b11, b12, b21, b22 = split(b)
    p1 = strassen(add(a11, a22), add(b11, b22))
    p2 = strassen(add(a21, a22), b11)
    p3 = strassen(a11, sub(b12, b22))
    p4 = strassen(a22, sub(b21, b11))
    p5 = strassen(add(a11, a12), b22)
    p6 = strassen(sub(a21, a11), add(b11, b12))
    p7 = strassen(sub(a12, a22), add(b21, b22))
    c11 = add(sub(add(p1, p4), p5), p7)
    c12 = add(p3, p5)
    c21 = add(p2, p4)
    c22 = add(sub(add(p1, p3), p2), p6)
    return combine(c11, c12, c21, c22)

def next_pow2(n):
    size = 1
    while size < n:
        size <<= 1
    return size

def pad(m, size):
    n = len(m)
    out = [[0] * size for _ in range(size)]
    for i in range(n):
        out[i][:n] = m[i]
    return out

def solve():
    first = input().strip()
    if not first:
        return
    n = int(first)
    a = [list(map(int, input().split())) for _ in range(n)]
    b = [list(map(int, input().split())) for _ in range(n)]
    size = next_pow2(n)
    result = strassen(pad(a, size), pad(b, size))
    trimmed = [row[:n] for row in result[:n]]
    print("\n".join(" ".join(map(str, row)) for row in trimmed))

if __name__ == "__main__":
    solve()
