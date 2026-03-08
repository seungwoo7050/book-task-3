import sys
input = sys.stdin.readline
sys.setrecursionlimit(200000)

def solve():
    n, m, r = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    # Sort each neighbor list ascending for deterministic order
    for i in range(1, n + 1):
        adj[i].sort()

    visited = [False] * (n + 1)
    result = [0] * (n + 1)
    order = [0]  # mutable counter

    def dfs(u):
        order[0] += 1
        result[u] = order[0]
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs(v)

    dfs(r)
    print('\n'.join(str(result[i]) for i in range(1, n + 1)))

if __name__ == "__main__":
    solve()
