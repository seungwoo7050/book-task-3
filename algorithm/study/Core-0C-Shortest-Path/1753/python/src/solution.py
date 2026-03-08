import sys, heapq
input = sys.stdin.readline
INF = float('inf')

def main():
    v, e = map(int, input().split())
    k = int(input())
    adj = [[] for _ in range(v + 1)]
    for _ in range(e):
        u, nv, w = map(int, input().split())
        adj[u].append((nv, w))
    dist = [INF] * (v + 1)
    dist[k] = 0
    hq = [(0, k)]
    while hq:
        d, u = heapq.heappop(hq)
        if d > dist[u]:
            continue
        for nv, w in adj[u]:
            nd = d + w
            if nd < dist[nv]:
                dist[nv] = nd
                heapq.heappush(hq, (nd, nv))
    out = []
    for i in range(1, v + 1):
        out.append(str(dist[i]) if dist[i] != INF else 'INF')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
