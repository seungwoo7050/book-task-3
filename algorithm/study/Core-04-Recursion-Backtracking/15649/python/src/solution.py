import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    used = [False] * (n + 1)
    seq = []
    out = []

    def backtrack(depth):
        if depth == m:
            out.append(' '.join(map(str, seq)))
            return
        for i in range(1, n + 1):
            if not used[i]:
                used[i] = True
                seq.append(i)
                backtrack(depth + 1)
                seq.pop()
                used[i] = False

    backtrack(0)
    print('\n'.join(out))

if __name__ == "__main__":
    solve()
