# 0x15 String Matching — 접근 과정

## KMP: Prefix Function

```python
pi = [0] * m
k = 0
for i in range(1, m):
    while k and pattern[k] != pattern[i]:
        k = pi[k-1]
    if pattern[k] == pattern[i]:
        k += 1
    pi[i] = k
```

`pi[i]` = pattern[0..i]의 최장 proper prefix-suffix 길이. 불일치 시 `pi[k-1]`로 점프하여 중복 비교 회피.

## KMP: 매칭

텍스트를 순회하며 패턴과 비교. 불일치 시 `pi[]` 활용 — 처음부터 다시 비교하지 않음.

## Rabin-Karp: Rolling Hash

- base = 257, mod = $10^9 + 7$
- 패턴 해시값 미리 계산
- 텍스트 윈도우 해시를 슬라이딩: `h = (h - ord(t[i]) * high) * base + ord(t[i+m])`
- 해시 충돌 시 실제 문자열 비교로 검증

```python
high = pow(base, m - 1, mod)
```
