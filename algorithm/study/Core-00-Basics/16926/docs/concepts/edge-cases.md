# 경계 사례 점검 — BOJ 16926 Array Rotation 1

## Constraints Recap

- $2 \le N, M \le 300$, $\min(N,M)$ is even
- $1 \le R \le 10^9$
- $1 \le A_{i,j} \le 10^8$

## 경계 사례 점검

### 1. R equals the layer perimeter (full cycle)

When $R \bmod L_k = 0$ for all layers, the array should remain unchanged.

**Example**: $4 \times 4$ matrix, $R = 12$ (outer ring has 12 elements)  
→ Outer ring returns to original position.

### 2. R much larger than perimeter

$R = 10^9$ with a small matrix. Without modular arithmetic, this would require $10^9$ element shifts.
Modular reduction brings the effective rotation to $R \bmod L$, which is at most $L - 1$.

### 3. Minimum matrix size (2×2)

Only one layer with 4 elements:
```
1 2    →  R=1  →  2 4
3 4              1 3
```

### 4. Non-square matrix (e.g., 2×4)

One layer with $2(2+4)-4 = 8$ elements:
```
1 2 3 4    →  R=1  →  2 3 4 8
5 6 7 8              1 6 7 5  ← Wait, check carefully
```
Ring: `[1,2,3,4,8,7,6,5]` → shift left by 1 → `[2,3,4,8,7,6,5,1]`
```
2 3 4 8
1 6 5 7  ← No, need to trace write-back carefully
```
Write back: top `[2,3,4,8]`, right `[7]`, bottom `[6,5]`, left `[1]`
```
2 3 4 8
1 6 5 7
```
This tests non-square handling where the four segments have different lengths.

### 5. Tall matrix (e.g., 6×2)

Only one layer with $2(6+2)-4 = 12$ elements. The top/bottom rows are short (2 elements each), while the columns are long (4 elements each).

### 6. Multiple layers with different perimeters

$6 \times 6$ matrix: 3 layers with perimeters 20, 12, and 4.
$R = 12$ → outer rotates by $12 \bmod 20 = 12$, middle rotates by $12 \bmod 12 = 0$, inner rotates by $12 \bmod 4 = 0$.

### 7. R = 1 (minimal rotation)

Each ring shifts by exactly one position counterclockwise. Good for verifying basic correctness.

## 요약

| # | Case | Key Test |
| :--- | :--- | :--- |
| 1 | Full cycle | Modular yields 0 → no change |
| 2 | Huge R | Modular arithmetic correctness |
| 3 | 2×2 matrix | Minimum size boundary |
| 4 | Non-square | Asymmetric segment lengths |
| 5 | Tall matrix | Long columns, short rows |
| 6 | Multi-layer, different periods | Per-layer modular independence |
| 7 | R = 1 | Basic single-step rotation |
