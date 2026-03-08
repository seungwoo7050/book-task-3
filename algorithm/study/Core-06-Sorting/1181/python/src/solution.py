import sys
input = sys.stdin.readline

def main():
    N = int(input())
    words = set(input().strip() for _ in range(N))
    # Sort by length first, then lexicographically
    result = sorted(words, key=lambda w: (len(w), w))
    print('\n'.join(result))

if __name__ == "__main__":
    main()
