import sys
from collections import deque
input = sys.stdin.readline

def main():
    n = int(input())
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    parent = [0] * (n + 1)
    visited = [False] * (n + 1)
    visited[1] = True
    q = deque([1])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                q.append(v)
    out = []
    for i in range(2, n + 1):
        out.append(str(parent[i]))
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
