import sys, heapq
input = sys.stdin.readline
INF = float('inf')

def main():
    n = int(input())
    m = int(input())
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, input().split())
        adj[u].append((v, w))
    s, e = map(int, input().split())
    dist = [INF] * (n + 1)
    dist[s] = 0
    hq = [(0, s)]
    while hq:
        d, u = heapq.heappop(hq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(hq, (nd, v))
    print(dist[e])

if __name__ == "__main__":
    main()
