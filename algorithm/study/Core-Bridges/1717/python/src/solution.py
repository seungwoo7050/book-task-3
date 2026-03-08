import sys


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent, a, b):
    ra = find(parent, a)
    rb = find(parent, b)
    if ra == rb:
        return
    if ra < rb:
        parent[rb] = ra
    else:
        parent[ra] = rb


def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    parent = list(range(n + 1))
    out = []
    for _ in range(m):
        op, a, b = map(int, input().split())
        if op == 0:
            union(parent, a, b)
        else:
            out.append("YES" if find(parent, a) == find(parent, b) else "NO")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
