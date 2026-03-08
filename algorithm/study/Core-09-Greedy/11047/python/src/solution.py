import sys
input = sys.stdin.readline

def main():
    N, K = map(int, input().split())
    coins = [int(input()) for _ in range(N)]

    count = 0
    for coin in reversed(coins):
        count += K // coin
        K %= coin

    print(count)

if __name__ == "__main__":
    main()
