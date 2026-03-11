import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # dp[i] = i에서 끝나는 LIS 길이
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if a[j] < a[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    print(max(dp))

if __name__ == "__main__":
    solve()
