import sys
input = sys.stdin.readline

def solve():
    word = input().strip()
    # A palindrome reads the same forwards and backwards
    print(1 if word == word[::-1] else 0)

if __name__ == "__main__":
    solve()
