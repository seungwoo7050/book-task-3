import sys
input = sys.stdin.readline

def main():
    N = int(input())
    pos = []   # 1보다 큰 수
    ones = 0
    neg = []   # 0보다 작은 수
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

    total = ones  # 값 1은 그대로 더한다

    # 양수는 가장 큰 값부터 둘씩 묶는다
    pos.sort(reverse=True)
    for i in range(0, len(pos) - 1, 2):
        total += pos[i] * pos[i + 1]
    if len(pos) % 2 == 1:
        total += pos[-1]

    # 음수는 가장 작은 값부터 둘씩 묶는다
    neg.sort()
    for i in range(0, len(neg) - 1, 2):
        total += neg[i] * neg[i + 1]
    if len(neg) % 2 == 1:
        # 0이 있으면 남은 음수를 상쇄하고, 없으면 그대로 더한다
        if zeros == 0:
            total += neg[-1]

    print(total)

if __name__ == "__main__":
    main()
