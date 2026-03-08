import sys
from collections import deque
input = sys.stdin.readline

def main():
    sys.setrecursionlimit(200000)
    v = int(input())
    adj = [[] for _ in range(v + 1)]
    for _ in range(v):
        data = list(map(int, input().split()))
        node = data[0]
        i = 1
        while data[i] != -1:
            neighbor, weight = data[i], data[i + 1]
            adj[node].append((neighbor, weight))
            i += 2

    def bfs(start):
        dist = [-1] * (v + 1)
        dist[start] = 0
        q = deque([start])
        far_node, far_dist = start, 0
        while q:
            u = q.popleft()
            for nv, w in adj[u]:
                if dist[nv] == -1:
                    dist[nv] = dist[u] + w
                    q.append(nv)
                    if dist[nv] > far_dist:
                        far_dist = dist[nv]
                        far_node = nv
        return far_node, far_dist

    u, _ = bfs(1)
    _, diameter = bfs(u)
    print(diameter)

if __name__ == "__main__":
    main()
