import sys
from collections import deque
input = sys.stdin.readline

def solve():
    first = input().strip()
    if not first:
        return
    n, m, s, t = map(int, first.split())
    cap = [[0] * (n + 1) for _ in range(n + 1)]
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, c = map(int, input().split())
        cap[u][v] += c
        adj[u].append(v)
        adj[v].append(u)
    flow = 0
    while True:
        parent = [-1] * (n + 1)
        parent[s] = s
        q = deque([s])
        while q and parent[t] == -1:
            u = q.popleft()
            for v in adj[u]:
                if parent[v] == -1 and cap[u][v] > 0:
                    parent[v] = u
                    q.append(v)
        if parent[t] == -1:
            break
        aug = 10 ** 18
        v = t
        while v != s:
            u = parent[v]
            aug = min(aug, cap[u][v])
            v = u
        v = t
        while v != s:
            u = parent[v]
            cap[u][v] -= aug
            cap[v][u] += aug
            v = u
        flow += aug
    print(flow)

if __name__ == "__main__":
    solve()
