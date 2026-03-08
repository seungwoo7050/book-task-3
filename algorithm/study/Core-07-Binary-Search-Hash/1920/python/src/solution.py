import sys
input = sys.stdin.readline

def main():
    N = int(input())
    A = set(map(int, input().split()))
    M = int(input())
    queries = list(map(int, input().split()))

    out = []
    for q in queries:
        out.append('1' if q in A else '0')
    print('\n'.join(out))

if __name__ == "__main__":
    main()
