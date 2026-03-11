import sys
input = sys.stdin.readline

def main():
    N = int(input())
    meetings = [tuple(map(int, input().split())) for _ in range(N)]
    # 종료 시간 우선, 같으면 시작 시간 순으로 정렬
    meetings.sort(key=lambda x: (x[1], x[0]))

    count = 0
    last_end = 0
    for start, end in meetings:
        if start >= last_end:
            count += 1
            last_end = end

    print(count)

if __name__ == "__main__":
    main()
