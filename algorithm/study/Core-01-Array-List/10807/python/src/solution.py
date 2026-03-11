import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    v = int(input())
    # 배열에서 v의 등장 횟수를 센다
    print(arr.count(v))

if __name__ == "__main__":
    solve()
