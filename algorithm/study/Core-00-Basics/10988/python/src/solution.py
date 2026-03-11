import sys
input = sys.stdin.readline

def solve():
    word = input().strip()
    # 회문은 앞에서 읽어도 뒤에서 읽어도 같다.
    print(1 if word == word[::-1] else 0)

if __name__ == "__main__":
    solve()
