import sys
input = sys.stdin.readline

def solve_set_cover():
    n, m = map(int, input().split())
    universe = set(range(1, n + 1))
    sets = []
    for _ in range(m):
        parts = list(map(int, input().split()))
        sets.append(set(parts[1:1 + parts[0]]))
    uncovered = set(universe)
    chosen = []
    while uncovered:
        best_idx = None
        best_cover = set()
        for idx, s in enumerate(sets, start=1):
            cover = s & uncovered
            if len(cover) > len(best_cover):
                best_idx = idx
                best_cover = cover
        if not best_cover:
            break
        chosen.append(best_idx)
        uncovered -= best_cover
    return " ".join(map(str, chosen)) if chosen else "NONE"

def solve_vertex_cover():
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    covered = [False] * m
    chosen = set()
    for i, (u, v) in enumerate(edges):
        if covered[i] or u in chosen or v in chosen:
            covered[i] = True
            continue
        chosen.add(u)
        chosen.add(v)
        for j, (a, b) in enumerate(edges):
            if a in chosen or b in chosen:
                covered[j] = True
    return " ".join(map(str, sorted(chosen))) if chosen else "NONE"

def solve():
    mode = input().strip().upper()
    if not mode:
        return
    if mode == "SET_COVER":
        print(solve_set_cover())
    elif mode == "VERTEX_COVER":
        print(solve_vertex_cover())
    else:
        raise ValueError(mode)

if __name__ == "__main__":
    solve()
