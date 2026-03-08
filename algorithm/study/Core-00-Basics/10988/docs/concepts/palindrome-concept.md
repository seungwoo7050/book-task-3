# Palindrome — Concept & Background

## Definition

A **palindrome** is a string that reads the same forwards and backwards.
More formally, a string $s$ of length $n$ is a palindrome if and only if:

$$s[i] = s[n - 1 - i] \quad \forall\, i \in [0, \lfloor n/2 \rfloor)$$

### Single-character & empty strings

- A single-character string is trivially a palindrome.
- An empty string is also considered a palindrome by convention.

## Examples

| Word | Palindrome? | Reason |
| :--- | :---: | :--- |
| `level` | Yes | `l-e-v-e-l` mirrors around the center `v` |
| `racecar` | Yes | `r-a-c-e-c-a-r` mirrors around `e` |
| `a` | Yes | Single character |
| `ab` | No | `a ≠ b` |
| `baekjoon` | No | `b ≠ n` at positions 0 and 7 |

## Odd vs Even Length

- **Odd length** (e.g. `aba`): There is a unique center character. It does not need to match anything.
- **Even length** (e.g. `abba`): Every character must have a matching partner on the opposite side.

## Why Palindromes Matter

Palindrome detection is a foundational problem in computer science and appears frequently in:

1. **String algorithms** — Manacher's algorithm finds all palindromic substrings in $O(n)$.
2. **Dynamic programming** — Longest palindromic subsequence is a classic DP problem.
3. **Interview prep** — Palindrome-related problems are among the most common coding interview questions.
4. **Formal language theory** — The set of palindromes over an alphabet is a context-free language but not regular.

## Connection to CLRS

| Chapter | Relevance |
| :--- | :--- |
| Ch 2 (Getting Started) | Loop invariants for correctness proofs of comparison-based techniques |
| Ch 3 (Growth of Functions) | Asymptotic analysis of $O(n)$ vs $O(n^2)$ palindrome checks |
| Ch 15 (Dynamic Programming) | Longest palindromic subsequence problem |

For this Bronze-level problem, only Ch 2–3 concepts are needed.

## Further Reading

- [Wikipedia — Palindrome](https://en.wikipedia.org/wiki/Palindrome)
- CLRS 4th ed., Section 2.1 (Insertion Sort) for loop invariant reasoning
- [Manacher's Algorithm](https://en.wikipedia.org/wiki/Longest_palindromic_substring#Manacher's_algorithm) (advanced)
