# Array & Linear Search — Concept & Background

## Array Fundamentals

An **array** is a contiguous block of memory storing elements of the same type, accessed by index. It is the most fundamental data structure in computer science.

### Key Properties

| Property | Value |
| :--- | :--- |
| Access by index | $O(1)$ |
| Search (unsorted) | $O(n)$ |
| Insert at end | $O(1)$ amortized (dynamic array) |
| Insert at position | $O(n)$ |
| Delete | $O(n)$ |

### Python Lists vs C++ Vectors

| Feature | Python `list` | C++ `vector` |
| :--- | :--- | :--- |
| Type | Dynamic, heterogeneous | Dynamic, homogeneous |
| Access | `a[i]` — $O(1)$ | `a[i]` — $O(1)$ |
| Count | `a.count(v)` — $O(n)$ | `std::count(begin, end, v)` — $O(n)$ |
| Append | `a.append(x)` — $O(1)$ amortized | `a.push_back(x)` — $O(1)$ amortized |

## Linear Search (Sequential Scan)

The simplest search algorithm: examine every element until the target is found or the array is exhausted.

```
LINEAR-SEARCH(A, v):
    count = 0
    for i = 0 to n-1:
        if A[i] == v:
            count += 1
    return count
```

### Why Linear Search Matters

- It is the **baseline** for all search algorithms
- For unsorted data, no algorithm can do better than $O(n)$ in the worst case
- Understanding it is prerequisite for appreciating binary search ($O(\log n)$), hash tables ($O(1)$ average), etc.

## CLRS Connection

| Chapter | Relevance |
| :--- | :--- |
| Ch 10 (Elementary Data Structures) | Arrays as contiguous storage; stack/queue operations on arrays |
| Ch 2.1 (Insertion Sort) | Linear scan as part of the insertion step |
| Ex 2.1-3 | Linear search problem — find index of target value |

## Applications

1. **Counting**: Count occurrences of a value (this problem)
2. **Filtering**: Extract elements matching a predicate
3. **Aggregation**: Sum, min, max, average — all require linear scan
4. **Validation**: Check if an element exists
