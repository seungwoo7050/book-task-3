import sys
import heapq
input = sys.stdin.readline

def main():
    N = int(input())
    heap = []  # min-heap; negate values for max-heap behavior
    out = []

    for _ in range(N):
        x = int(input())
        if x > 0:
            heapq.heappush(heap, -x)
        else:
            if heap:
                out.append(str(-heapq.heappop(heap)))
            else:
                out.append('0')

    print('\n'.join(out))

if __name__ == "__main__":
    main()
