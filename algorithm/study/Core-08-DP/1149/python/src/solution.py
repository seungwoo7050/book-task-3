import sys
input = sys.stdin.readline

def main():
    N = int(input())
    # prev[c] = 이전 집까지 칠했을 때 마지막 색이 c인 최소 비용
    prev = list(map(int, input().split()))

    for _ in range(N - 1):
        cost = list(map(int, input().split()))
        curr = [
            cost[0] + min(prev[1], prev[2]),
            cost[1] + min(prev[0], prev[2]),
            cost[2] + min(prev[0], prev[1]),
        ]
        prev = curr

    print(min(prev))

if __name__ == "__main__":
    main()
