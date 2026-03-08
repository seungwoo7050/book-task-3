# LIS (Longest Increasing Subsequence) — Concept & Background

## Definition

Given a sequence $A = [a_1, a_2, \dots, a_n]$, a **subsequence** is any sequence obtained by deleting zero or more elements without changing the relative order.

An **increasing subsequence** is a subsequence $a_{i_1}, a_{i_2}, \dots, a_{i_k}$ where:
- $i_1 < i_2 < \dots < i_k$ (positions are in order)
- $a_{i_1} < a_{i_2} < \dots < a_{i_k}$ (values are strictly increasing)

The **LIS** is the increasing subsequence of maximum length.

## Example

$A = [10, 20, 10, 30, 20, 50]$

Some increasing subsequences:
- $[10, 20]$ (length 2)
- $[10, 20, 30]$ (length 3)
- $[10, 20, 30, 50]$ (length 4) ← **LIS**

Note: The LIS is not necessarily unique. $[10, 20, 30, 50]$ can be formed starting from index 0 or index 2.

## Why LIS Matters

LIS is one of the most fundamental dynamic programming problems:

1. **Algorithm design education**: It demonstrates optimal substructure and overlapping subproblems.
2. **Practical applications**:
   - Version control: finding the longest common unchanged sequence
   - Patience sorting: a card sorting algorithm directly related to LIS
   - Bioinformatics: sequence alignment
3. **Complexity analysis**: The contrast between $O(n^2)$ DP and $O(n \log n)$ binary search solutions is instructive.

## Two Classical Approaches

### 1. $O(n^2)$ DP

Define $dp[i]$ = length of LIS ending at position $i$.

$$dp[i] = 1 + \max\{dp[j] : j < i,\; A[j] < A[i]\}$$

Answer: $\max_i dp[i]$

### 2. $O(n \log n)$ with Binary Search

Maintain a `tails` array where `tails[k]` = smallest tail element of all increasing subsequences of length $k+1$.

For each element, either extend `tails` (if larger than all) or replace (using `bisect_left`).

## CLRS Connection

| Chapter | Relevance |
| :--- | :--- |
| Ch 15 (Dynamic Programming) | LIS is a direct application of DP. Optimal substructure: best LIS ending at $i$ extends some best LIS ending at $j < i$. |
| Ch 15.4 (LCS) | LIS can be reduced to LCS of the original sequence and its sorted version. |
| Ch 3 (Growth of Functions) | $O(n^2)$ vs $O(n \log n)$: when $n$ changes from $10^3$ to $10^5$, the faster algorithm becomes necessary. |

## Related Problems

- **Longest Non-decreasing Subsequence**: Change strict inequality to $\le$
- **Longest Decreasing Subsequence**: Reverse the array and find LIS
- **Number of LIS**: Count all LIS of maximum length (requires additional DP array)
- **LIS with actual sequence**: Track predecessors for recovery

## Further Reading

- CLRS 4th ed., Chapter 15 — Dynamic Programming
- [Wikipedia — Longest Increasing Subsequence](https://en.wikipedia.org/wiki/Longest_increasing_subsequence)
- Patience Sorting and its connection to LIS
