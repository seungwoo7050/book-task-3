import sys
input = sys.stdin.readline

def main():
    N = int(input())
    segments = [tuple(map(int, input().split())) for _ in range(N)]
    segments.sort()

    total = 0
    cur_start, cur_end = segments[0]

    for s, e in segments[1:]:
        if s <= cur_end:
            # 겹치거나 맞닿으면 현재 구간을 늘린다
            cur_end = max(cur_end, e)
        else:
            # 빈 구간이 생기면 현재 구간을 확정한다
            total += cur_end - cur_start
            cur_start, cur_end = s, e

    # 마지막 구간을 더한다.
    total += cur_end - cur_start
    print(total)

if __name__ == "__main__":
    main()
