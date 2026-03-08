import sys
from collections import deque
input = sys.stdin.readline
sys.setrecursionlimit(10000)

def solve():
    n, m, v = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)
    for i in range(1, n + 1):
        adj[i].sort()

    # DFS
    dfs_order = []
    visited = [False] * (n + 1)

    def dfs(u):
        visited[u] = True
        dfs_order.append(u)
        for w in adj[u]:
            if not visited[w]:
                dfs(w)

    dfs(v)

    # BFS
    bfs_order = []
    visited = [False] * (n + 1)
    q = deque([v])
    visited[v] = True
    while q:
        u = q.popleft()
        bfs_order.append(u)
        for w in adj[u]:
            if not visited[w]:
                visited[w] = True
                q.append(w)

    print(' '.join(map(str, dfs_order)))
    print(' '.join(map(str, bfs_order)))

if __name__ == "__main__":
    solve()
