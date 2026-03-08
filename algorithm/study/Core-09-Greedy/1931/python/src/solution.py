import sys
input = sys.stdin.readline

def main():
    N = int(input())
    meetings = [tuple(map(int, input().split())) for _ in range(N)]
    # Sort by end time, then by start time
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
