import sys
from collections import Counter
input = sys.stdin.readline

def main():
    N = int(input())
    cards = list(map(int, input().split()))
    M = int(input())
    queries = list(map(int, input().split()))

    cnt = Counter(cards)
    print(' '.join(str(cnt[q]) for q in queries))

if __name__ == "__main__":
    main()
