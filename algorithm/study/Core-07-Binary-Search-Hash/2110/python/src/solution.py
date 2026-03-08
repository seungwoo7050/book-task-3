import sys
input = sys.stdin.readline

def main():
    N, C = map(int, input().split())
    houses = sorted(int(input()) for _ in range(N))

    def feasible(d):
        """Can we place C routers with min distance >= d?"""
        count = 1
        last = houses[0]
        for i in range(1, N):
            if houses[i] - last >= d:
                count += 1
                last = houses[i]
                if count >= C:
                    return True
        return False

    lo, hi, ans = 1, houses[-1] - houses[0], 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    main()
