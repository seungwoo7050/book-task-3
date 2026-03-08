# Keylogger & Cursor Simulation — Concept & Background

## Problem Context

A **keylogger** captures raw keystrokes including special keys (cursor movement, backspace). Reconstructing the actual typed text requires simulating the cursor behavior — the same fundamental problem as a text editor (BOJ 1406).

## Relationship to BOJ 1406 (Editor)

| Aspect | BOJ 1406 (Editor) | BOJ 5397 (Keylogger) |
| :--- | :--- | :--- |
| Move left | `L` | `<` |
| Move right | `D` | `>` |
| Backspace | `B` | `-` |
| Insert | `P x` | any other char |
| Multiple test cases | No | Yes ($T \le 1{,}000$) |
| Max total input | ~600K | ~5M |

The algorithm is identical; only the command symbols and I/O scale differ.

## Two-Stack Technique (Recap)

```
Password view:  H e l | l o
                ←left→  ←right→ (reversed)
left  = [H, e, l]
right = [o, l]
```

All operations map to stack `push`/`pop` → $O(1)$ each.

## Scaling Considerations

With total input up to $5 \times 10^6$ characters:
- **Python**: Must use `sys.stdin.readline` and `sys.stdout.write` for I/O
- **C++**: `ios_base::sync_with_stdio(false)` is essential
- **Array insert**: Would result in $O(N^2)$ per test case → catastrophic TLE

## CLRS Connection

| Chapter | Relevance |
| :--- | :--- |
| Ch 10.1 | Stack ADT: LIFO semantics power the two-stack cursor model |
| Ch 10.2 | Linked list: C++ `std::list` solution directly implements CLRS's doubly-linked list |
| Ch 17 (Amortized Analysis) | Python list `append`/`pop` are $O(1)$ amortized due to dynamic array doubling |
