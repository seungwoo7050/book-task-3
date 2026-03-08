import sys
input = sys.stdin.readline

def main():
    N, K = map(int, input().split())
    dp = [0] * (K + 1)

    for _ in range(N):
        w, v = map(int, input().split())
        # Iterate in reverse to ensure 0/1 property
        for j in range(K, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + v)

    print(dp[K])

if __name__ == "__main__":
    main()
