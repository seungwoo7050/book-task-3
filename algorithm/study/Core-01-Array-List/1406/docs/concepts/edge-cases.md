# Edge Cases — BOJ 1406 Editor

## Constraints Recap
- Initial string length: $\le 100{,}000$
- Commands: $M \le 500{,}000$

## Edge Case Analysis

### 1. Cursor at Start — L and B Ignored
Cursor is at position 0. `L` and `B` should do nothing.

### 2. Cursor at End — D Ignored
Cursor is at the end. `D` should do nothing.

### 3. Empty String After Deletions
Delete all characters via repeated `B`. The result should be an empty string or contain only inserted characters.

### 4. All Insertions
$M$ consecutive `P x` commands with no movement. All characters are inserted at the end.

### 5. Large Input ($N + M \approx 600{,}000$)
Tests that the solution is $O(N + M)$ and not $O(NM)$.

### 6. Mixed Operations with Cursor at Various Positions
Rapid alternation of L, D, P, B — tests that stack operations are correctly paired.

### 7. Insert and Immediately Delete
`P x` followed by `B` should cancel out.

## Summary

| # | Case | Key Test |
| :--- | :--- | :--- |
| 1 | Cursor at start | Boundary guard on L, B |
| 2 | Cursor at end | Boundary guard on D |
| 3 | All deleted | Empty result handling |
| 4 | All insertions | Append-only pattern |
| 5 | Max input | Performance: $O(N+M)$ |
| 6 | Mixed ops | Stack consistency |
| 7 | Insert + delete | Operation cancellation |
