import sys
input = sys.stdin.readline
INF = float('inf')

def main():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        edges.append((a, b, c))
    dist = [INF] * (n + 1)
    dist[1] = 0
    for i in range(n):
        for a, b, c in edges:
            if dist[a] != INF and dist[a] + c < dist[b]:
                if i == n - 1:
                    print(-1)
                    return
                dist[b] = dist[a] + c
    out = []
    for i in range(2, n + 1):
        out.append(str(dist[i]) if dist[i] != INF else '-1')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
