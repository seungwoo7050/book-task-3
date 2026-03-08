import sys
input = sys.stdin.readline

def main():
    n = int(input())
    if n <= 1:
        print(n)
        return

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    print(b)

if __name__ == "__main__":
    main()
