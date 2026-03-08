# Two-Stack Editor & Linked List — Concept & Background

## The Editor Problem

A text editor with a movable cursor requires efficient:
- **Insertion** at cursor position
- **Deletion** at cursor position
- **Cursor movement** left/right

### Naive Approach: Array with Index

```python
text = list("abcd")
cursor = 4  # after 'd'
# Insert 'x' at cursor: text.insert(cursor, 'x') → O(N) shift!
```

This is $O(N)$ per insert/delete due to element shifting. With $M = 500{,}000$ commands, this results in up to $5 \times 10^{10}$ operations → **TLE**.

## Solution 1: Two-Stack Model

Split the text at the cursor into two stacks:

```
Text:   a b c | d e f
        ←left→  ←right→
left  = [a, b, c]     (top = c, closest to cursor)
right = [f, e, d]     (top = d, closest to cursor)
```

### Operations

| Command | Action | Time |
| :--- | :--- | :--- |
| `L` (left) | `right.push(left.pop())` | $O(1)$ |
| `D` (right) | `left.push(right.pop())` | $O(1)$ |
| `B` (delete) | `left.pop()` | $O(1)$ |
| `P x` (insert) | `left.push(x)` | $O(1)$ |

### Reconstruction

Final string = `left` (bottom → top) + `right` (top → bottom = reversed)

## Solution 2: Doubly-Linked List + Iterator

```cpp
list<char> L(s.begin(), s.end());
auto cursor = L.end();
```

Each operation directly manipulates the list:
- `L`: `--cursor`
- `D`: `++cursor`  
- `B`: `L.erase(prev(cursor))`
- `P x`: `L.insert(cursor, x)`

All $O(1)$ thanks to pointer manipulation.

## Comparison

| Aspect | Two-Stack (Python) | Linked List (C++) |
| :--- | :--- | :--- |
| Time per op | $O(1)$ amortized | $O(1)$ |
| Space overhead | Minimal (two lists) | Node pointers (prev/next) |
| Cache efficiency | Better (contiguous memory) | Worse (scattered nodes) |
| Implementation | Very simple | Moderate |

## CLRS Connection

| Chapter | Relevance |
| :--- | :--- |
| Ch 10.1 (Stacks & Queues) | The two-stack model uses LIFO semantics for bidirectional traversal |
| Ch 10.2 (Linked Lists) | Doubly-linked list enables $O(1)$ insert/delete at any position with a pointer |
| Ch 10.2 (Sentinels) | `list.end()` acts as a sentinel node in C++ STL |

## Why This Problem Matters

This problem teaches that **data structure choice determines performance**:
- Array-based: $O(NM)$ → TLE
- Stack/List-based: $O(N + M)$ → passes easily

This is one of the classic problems where the "obvious" array approach fails and a deeper understanding of data structures is required.
