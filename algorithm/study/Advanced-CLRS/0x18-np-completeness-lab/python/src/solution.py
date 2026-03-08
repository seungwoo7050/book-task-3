import sys
input = sys.stdin.readline

def verify_vc():
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    k = int(input())
    cert = set(map(int, input().split())) if k else set()
    return all(u in cert or v in cert for u, v in edges)

def verify_3sat():
    n_vars, n_clauses = map(int, input().split())
    clauses = [list(map(int, input().split())) for _ in range(n_clauses)]
    bits = input().strip()
    assign = {i + 1: bits[i] == '1' for i in range(n_vars)}
    for clause in clauses:
        ok = False
        for lit in clause:
            val = assign[abs(lit)]
            ok |= val if lit > 0 else (not val)
        if not ok:
            return False
    return True

def solve():
    mode = input().strip().upper()
    if not mode:
        return
    if mode == "VC":
        print("YES" if verify_vc() else "NO")
    elif mode == "3SAT":
        print("YES" if verify_3sat() else "NO")
    else:
        raise ValueError(mode)

if __name__ == "__main__":
    solve()
