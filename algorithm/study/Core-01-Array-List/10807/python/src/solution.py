import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    v = int(input())
    # Count occurrences of v in the array
    print(arr.count(v))

if __name__ == "__main__":
    solve()
