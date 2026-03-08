import sys
input = sys.stdin.readline

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def on_segment(a, b, p):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def intersect(a, b, c, d):
    ab_c = cross(a, b, c)
    ab_d = cross(a, b, d)
    cd_a = cross(c, d, a)
    cd_b = cross(c, d, b)
    if ab_c == ab_d == cd_a == cd_b == 0:
        return max(min(a[0], b[0]), min(c[0], d[0])) <= min(max(a[0], b[0]), max(c[0], d[0])) and max(min(a[1], b[1]), min(c[1], d[1])) <= min(max(a[1], b[1]), max(c[1], d[1]))
    if ab_c == 0 and on_segment(a, b, c):
        return True
    if ab_d == 0 and on_segment(a, b, d):
        return True
    if cd_a == 0 and on_segment(c, d, a):
        return True
    if cd_b == 0 and on_segment(c, d, b):
        return True
    return (ab_c > 0) != (ab_d > 0) and (cd_a > 0) != (cd_b > 0)

def solve():
    mode = input().strip().upper()
    if not mode:
        return
    if mode == "HULL":
        n = int(input())
        pts = [tuple(map(int, input().split())) for _ in range(n)]
        ans = hull(pts)
        print("\n".join(f"{x} {y}" for x, y in ans))
    elif mode == "INTERSECT":
        a = tuple(map(int, input().split()))
        b = tuple(map(int, input().split()))
        p1, p2 = (a[0], a[1]), (a[2], a[3])
        p3, p4 = (b[0], b[1]), (b[2], b[3])
        print("YES" if intersect(p1, p2, p3, p4) else "NO")
    else:
        raise ValueError(mode)

if __name__ == "__main__":
    solve()
