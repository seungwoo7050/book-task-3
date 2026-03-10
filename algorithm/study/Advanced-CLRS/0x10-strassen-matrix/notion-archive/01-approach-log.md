# 0x10 Strassen Matrix — 접근 과정

## Naive vs Strassen

- Naive: 3중 루프, $O(n^3)$
- Strassen: 행렬을 4개 부분으로 분할, 7번 곱셈 + 18번 덧셈/뺄셈

## 핵심 구현

1. **split**: 행렬을 4개 사분면으로 분할
2. **P1~P7**: 7개 보조 곱셈 (Strassen의 공식)
3. **combine**: 결과 조합
4. **pad**: 2의 거듭제곱으로 패딩
5. **베이스 케이스**: $n \leq 2$이면 naive

```python
p1 = strassen(add(a11, a22), add(b11, b22))
# ... p2~p7
c11 = add(sub(add(p1, p4), p5), p7)
```

## 시간 복잡도

$$T(n) = 7T(n/2) + O(n^2) = O(n^{\log_2 7}) \approx O(n^{2.807})$$
