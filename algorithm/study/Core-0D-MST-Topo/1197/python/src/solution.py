import sys
input = sys.stdin.readline

def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(parent, rank, a, b):
    a, b = find(parent, a), find(parent, b)
    if a == b:
        return False
    if rank[a] < rank[b]:
        a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]:
        rank[a] += 1
    return True

def main():
    v, e = map(int, input().split())
    edges = []
    for _ in range(e):
        a, b, c = map(int, input().split())
        edges.append((c, a, b))
    edges.sort()
    parent = list(range(v + 1))
    rank = [0] * (v + 1)
    total = 0
    cnt = 0
    for w, a, b in edges:
        if union(parent, rank, a, b):
            total += w
            cnt += 1
            if cnt == v - 1:
                break
    print(total)

if __name__ == "__main__":
    main()
