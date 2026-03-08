import sys, heapq
input = sys.stdin.readline

def main():
    n = int(input())
    heap = [int(input()) for _ in range(n)]
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        s = a + b
        total += s
        heapq.heappush(heap, s)
    print(total)

if __name__ == "__main__":
    main()
