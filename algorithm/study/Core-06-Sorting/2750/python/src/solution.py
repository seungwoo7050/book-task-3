import sys
input = sys.stdin.readline

def main():
    N = int(input())
    nums = [int(input()) for _ in range(N)]
    nums.sort()
    print('\n'.join(map(str, nums)))

if __name__ == "__main__":
    main()
