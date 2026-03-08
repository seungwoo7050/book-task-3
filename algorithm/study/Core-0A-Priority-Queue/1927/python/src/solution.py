import sys, heapq
input = sys.stdin.readline

def main():
    n = int(input())
    heap = []
    out = []
    for _ in range(n):
        x = int(input())
        if x:
            heapq.heappush(heap, x)
        else:
            out.append(str(heapq.heappop(heap)) if heap else '0')
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == "__main__":
    main()
