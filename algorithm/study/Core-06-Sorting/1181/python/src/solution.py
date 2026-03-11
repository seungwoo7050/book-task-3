import sys
input = sys.stdin.readline

def main():
    N = int(input())
    words = set(input().strip() for _ in range(N))
    # 길이 우선, 같으면 사전순으로 정렬
    result = sorted(words, key=lambda w: (len(w), w))
    print('\n'.join(result))

if __name__ == "__main__":
    main()
