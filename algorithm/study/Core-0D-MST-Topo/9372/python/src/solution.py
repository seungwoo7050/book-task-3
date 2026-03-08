import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        for _ in range(m):
            input()
        print(n - 1)

if __name__ == "__main__":
    main()
