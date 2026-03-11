import sys
from collections import deque
input = sys.stdin.readline

def main():
    # 4개의 톱니를 읽는다(각각 int deque)
    gears = [deque(int(c) for c in input().strip()) for _ in range(4)]

    K = int(input())
    for _ in range(K):
        num, d = map(int, input().split())
        num -= 1  # 0-based 인덱스

        # 각 톱니의 회전 방향을 결정
        dirs = [0] * 4
        dirs[num] = d

        # 왼쪽으로 회전을 전파
        for i in range(num - 1, -1, -1):
            if gears[i][2] != gears[i + 1][6]:
                dirs[i] = -dirs[i + 1]
            else:
                break  # 더 이상 전파되지 않음

        # 오른쪽으로 회전을 전파
        for i in range(num + 1, 4):
            if gears[i][6] != gears[i - 1][2]:
                dirs[i] = -dirs[i - 1]
            else:
                break

        # 회전을 적용한다.
        for i in range(4):
            if dirs[i] == 1:        # 시계 방향
                gears[i].appendleft(gears[i].pop())
            elif dirs[i] == -1:     # 반시계 방향
                gears[i].append(gears[i].popleft())

    # 점수를 계산
    score = sum(gears[i][0] * (1 << i) for i in range(4))
    print(score)

if __name__ == "__main__":
    main()
