# 경계 사례 점검 — BOJ 10807 Count Occurrences

## Constraints Recap

- $1 \le N \le 100$
- $-100 \le A_i \le 100$
- $-100 \le v \le 100$

## 경계 사례 점검

### 1. Target Not Present

**Input**: `3\n1 2 3\n5`  
**Expected**: `0`

The target $v$ does not appear at all.

### 2. All Elements Equal to Target

**Input**: `4\n7 7 7 7\n7`  
**Expected**: `4`

Every element matches.

### 3. Single Element — Match

**Input**: `1\n42\n42`  
**Expected**: `1`

Minimum $N$ with a match.

### 4. Single Element — No Match

**Input**: `1\n42\n99`  
**Expected**: `0`

Minimum $N$ with no match.

### 5. Negative Values

**Input**: `5\n-1 -2 -1 3 -1\n-1`  
**Expected**: `3`

Tests handling of negative integers.

### 6. Zero as Target

**Input**: `4\n0 1 0 2\n0`  
**Expected**: `2`

### 7. Maximum Size

**Input**: 100 elements, all equal to target  
**Expected**: `100`

## 요약

| # | Case | Expected | Key Test |
| :--- | :--- | :--- | :--- |
| 1 | Not present | 0 | Zero count |
| 2 | All match | N | Maximum count |
| 3 | Single, match | 1 | Min boundary (hit) |
| 4 | Single, no match | 0 | Min boundary (miss) |
| 5 | Negatives | varies | Negative number handling |
| 6 | Zero target | varies | Zero handling |
| 7 | Max size | 100 | Upper boundary |
