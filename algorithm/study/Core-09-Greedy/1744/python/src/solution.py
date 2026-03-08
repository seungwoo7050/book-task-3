import sys
input = sys.stdin.readline

def main():
    N = int(input())
    pos = []   # > 1
    ones = 0
    neg = []   # < 0
    zeros = 0

    for _ in range(N):
        x = int(input())
        if x > 1:
            pos.append(x)
        elif x == 1:
            ones += 1
        elif x == 0:
            zeros += 1
        else:
            neg.append(x)

    total = ones  # each 1 is added directly

    # Pair positives (largest with second-largest)
    pos.sort(reverse=True)
    for i in range(0, len(pos) - 1, 2):
        total += pos[i] * pos[i + 1]
    if len(pos) % 2 == 1:
        total += pos[-1]

    # Pair negatives (most negative with second-most negative)
    neg.sort()
    for i in range(0, len(neg) - 1, 2):
        total += neg[i] * neg[i + 1]
    if len(neg) % 2 == 1:
        # If there's a zero, pair with it (cancel out); otherwise add the negative
        if zeros == 0:
            total += neg[-1]

    print(total)

if __name__ == "__main__":
    main()
