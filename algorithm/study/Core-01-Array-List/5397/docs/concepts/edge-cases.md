# 경계 사례 점검 — BOJ 5397 Keylogger

## Constraints
- $T \le 1{,}000$ test cases
- Keystroke length per case $\le 1{,}000{,}000$
- Total across all cases $\le 5{,}000{,}000$

## 경계 사례 점검

### 1. All Special Keys — Empty Password
Input: `<<<--->>>` → No characters inserted → empty output line.

### 2. No Special Keys
Input: `password123` → Output as-is.

### 3. Extensive Backspacing
Input: `abc---` → Three chars inserted, three backspaces → empty.

### 4. Cursor Bouncing at Boundaries
Input: `a<<<<b` → left is `[a]`, then 4 `<` (only 1 effective), then `b` → `ba`.

### 5. Maximum Length Single Case
$10^6$ characters — tests $O(N)$ performance.

### 6. Many Short Test Cases
$T = 1{,}000$ each with ~5000 chars — tests per-case initialization overhead.

### 7. Insert-Move-Insert Pattern
`a>b<c` → final position depends on careful cursor tracking.

## 요약

| # | Case | Key Test |
| :--- | :--- | :--- |
| 1 | All special | Empty output |
| 2 | No special | Pass-through |
| 3 | Full backspace | Complete deletion |
| 4 | Boundary bounce | Guard clause correctness |
| 5 | Max length | Performance |
| 6 | Many cases | Initialization overhead |
| 7 | Interleaved ops | Cursor state tracking |
