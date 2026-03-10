# 경계 사례 점검 — BOJ 11053 Longest Increasing Subsequence

## Constraints Recap

- $1 \le N \le 1{,}000$
- $1 \le A_i \le 1{,}000$

## 경계 사례 점검

### 1. Single Element ($N = 1$)

**Input**: `1\n5`  
**Expected**: `1`

The LIS of a single element is trivially 1.

### 2. Already Sorted (Strictly Increasing)

**Input**: `5\n1 2 3 4 5`  
**Expected**: `5`

The entire sequence is the LIS. All `dp[i] = i + 1`.

### 3. Strictly Decreasing

**Input**: `5\n5 4 3 2 1`  
**Expected**: `1`

No two elements form an increasing pair. Every `dp[i] = 1`.

### 4. All Elements Equal

**Input**: `5\n3 3 3 3 3`  
**Expected**: `1`

Since LIS requires **strict** increase, equal elements don't count.

### 5. Maximum Length (N = 1000, All Increasing)

**Input**: `1000\n1 2 3 ... 1000`  
**Expected**: `1000`

Tests the upper boundary of $N$. The $O(N^2)$ approach does $10^6$ operations — well within time limits.

### 6. Alternating Sequence

**Input**: `6\n1 3 2 4 3 5`  
**Expected**: `4` (e.g., $[1, 2, 4, 5]$ or $[1, 3, 4, 5]$)

Tests that the algorithm correctly navigates "zigzag" patterns.

### 7. LIS Not Contiguous

**Input**: `7\n3 1 2 1 8 1 9`  
**Expected**: `4` (e.g., $[1, 2, 8, 9]$)

The LIS elements are scattered. Tests that the algorithm uses subsequences, not subarrays.

## 요약

| # | Case | N | Expected | Key Test |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Single element | 1 | 1 | Minimum boundary |
| 2 | Sorted ascending | 5 | 5 | Full-length LIS |
| 3 | Sorted descending | 5 | 1 | Worst case (all dp = 1) |
| 4 | All equal | 5 | 1 | Strict inequality check |
| 5 | Max N, ascending | 1000 | 1000 | Performance boundary |
| 6 | Alternating | 6 | 4 | Non-monotonic pattern |
| 7 | Scattered LIS | 7 | 4 | Subsequence vs subarray |
