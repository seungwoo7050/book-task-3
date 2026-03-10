# 0x17 Number Theory Lab — 접근 과정

## Extended GCD

```python
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y
```

$ax + by = \gcd(a, b)$ 의 해 $(x, y)$ 반환.

## 모듈러 역원

`modinv(a, m)`: $a \cdot x \equiv 1 \pmod{m}$ 인 $x$. `egcd(a, m)` 에서 gcd=1이면 `x % m`.

## CRT (중국인 나머지 정리)

합동식 $(r_1, m_1), (r_2, m_2), \ldots$ 를 반복적으로 병합:

$$x \equiv r_1 \pmod{m_1}, \quad x \equiv r_2 \pmod{m_2}$$

$\to$ $x \equiv r \pmod{\text{lcm}(m_1, m_2)}$

## Toy RSA

1. $n = p \times q$
2. $\phi = (p-1)(q-1)$
3. $d = e^{-1} \bmod \phi$
4. cipher = $m^e \bmod n$
5. plain = $\text{cipher}^d \bmod n$

Python `pow(m, e, n)` 으로 모듈러 거듭제곱.
