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
            # Overlapping or adjacent — extend
            cur_end = max(cur_end, e)
        else:
            # Gap — finalize current interval
            total += cur_end - cur_start
            cur_start, cur_end = s, e

    # Add the last interval
    total += cur_end - cur_start
    print(total)

if __name__ == "__main__":
    main()
