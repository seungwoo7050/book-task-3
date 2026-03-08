import sys
input = sys.stdin.readline

def kmp(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))
    pi = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
    out = []
    j = 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
            if j == len(pattern):
                out.append(i - len(pattern) + 1)
                j = pi[j - 1]
    return out

def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    base = 257
    mod = 1_000_000_007
    high = pow(base, m - 1, mod)
    p_hash = 0
    t_hash = 0
    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
    out = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            out.append(i)
        if i + m < n:
            t_hash = (t_hash - ord(text[i]) * high) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod
    return out

def solve():
    mode = input().strip().upper()
    if not mode:
        return
    text = input().rstrip("\n")
    pattern = input().rstrip("\n")
    if mode == "KMP":
        ans = kmp(text, pattern)
    elif mode == "RK":
        ans = rabin_karp(text, pattern)
    else:
        raise ValueError(mode)
    print(" ".join(map(str, ans)) if ans else "NONE")

if __name__ == "__main__":
    solve()
