import sys
input = sys.stdin.readline

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def crt(congruences):
    x = 0
    mod = 1
    for r, m in congruences:
        g, s, _ = egcd(mod, m)
        if (r - x) % g != 0:
            raise ValueError("Incompatible congruences")
        step = ((r - x) // g * s) % (m // g)
        x += mod * step
        mod = mod // g * m
        x %= mod
    return x, mod

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Inverse does not exist")
    return x % m

def solve():
    mode = input().strip().upper()
    if not mode:
        return
    if mode == "GCD":
        a, b = map(int, input().split())
        g, x, y = egcd(a, b)
        print(f"gcd={g} x={x} y={y}")
    elif mode == "CRT":
        k = int(input())
        congruences = [tuple(map(int, input().split())) for _ in range(k)]
        x, mod = crt(congruences)
        print(f"x={x} mod={mod}")
    elif mode == "RSA":
        p, q, e, m = map(int, input().split())
        n = p * q
        phi = (p - 1) * (q - 1)
        d = modinv(e, phi)
        cipher = pow(m, e, n)
        plain = pow(cipher, d, n)
        print(f"n={n} phi={phi} d={d} cipher={cipher} plain={plain}")
    else:
        raise ValueError(mode)

if __name__ == "__main__":
    solve()
