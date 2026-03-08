# Edge Cases — BOJ 10988 Palindrome Check

## Problem Constraints Recap

- Input: a single word of lowercase English letters
- Length: $1 \le |word| \le 100$

## Edge Case Analysis

### 1. Single Character

**Input:** `a`  
**Expected:** `1`

A single character is always a palindrome. This is the smallest valid input.

### 2. Two Identical Characters

**Input:** `aa`  
**Expected:** `1`

The simplest even-length palindrome.

### 3. Two Different Characters

**Input:** `ab`  
**Expected:** `0`

The simplest non-palindrome.

### 4. Maximum Length Palindrome

**Input:** `a` repeated 100 times  
**Expected:** `1`

Tests that the solution handles the maximum constraint correctly.

### 5. Maximum Length Non-palindrome

**Input:** 99 `a`s followed by `b`  
**Expected:** `0`

The mismatch occurs only at the outermost pair (positions 0 and 99).

### 6. Nearly Palindrome (Off by One Character)

**Input:** `abcba` → palindrome; `abcda` → not palindrome  

Ensures the solution checks every pair, not just the first/last.

### 7. All Same Characters

**Input:** `zzzzz`  
**Expected:** `1`

A string of identical characters is always a palindrome regardless of length.

## Summary

| # | Case | Length | Expected | Tests |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Single char | 1 | 1 | Minimum boundary |
| 2 | Two same | 2 | 1 | Even-length palindrome |
| 3 | Two different | 2 | 0 | Even-length non-palindrome |
| 4 | Max palindrome | 100 | 1 | Upper boundary |
| 5 | Max non-palindrome | 100 | 0 | Mismatch at boundary |
| 6 | Near-palindrome | 5 | 0 | Interior mismatch |
| 7 | Uniform string | any | 1 | Degenerate case |

For a Bronze-tier problem, the constraints are small enough that correctness is the only concern — no performance edge cases exist.
