# Layer Decomposition — Concept & Background

## What is Layer Decomposition?

In the context of 2D array rotation, **layer decomposition** is the technique of viewing an $N \times M$ matrix as a set of concentric rectangular rings (layers), each of which can be manipulated independently.

### Visual Example

For a $4 \times 4$ matrix:

```
Layer 0 (outermost):          Layer 1 (inner):
 1  2  3  4                      .  .  .  .
 5  .  .  8      →               .  6  7  .
 9  .  . 12                      . 10 11  .
13 14 15 16                      .  .  .  .
```

Layer 0 contains: `[1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5]`  
Layer 1 contains: `[6, 7, 11, 10]`

### Number of Layers

$$\text{layers} = \lfloor \min(N, M) / 2 \rfloor$$

The problem guarantees $\min(N, M)$ is even, so every element belongs to exactly one layer.

## Layer Extraction Order

For layer $k$ (0-indexed from the outermost):

| Segment | Traversal | Coordinates |
| :--- | :--- | :--- |
| Top row | Left → Right | $(k, k)$ to $(k, M{-}1{-}k)$ |
| Right column | Top → Bottom | $(k{+}1, M{-}1{-}k)$ to $(N{-}1{-}k, M{-}1{-}k)$ |
| Bottom row | Right → Left | $(N{-}1{-}k, M{-}2{-}k)$ to $(N{-}1{-}k, k)$ |
| Left column | Bottom → Top | $(N{-}2{-}k, k)$ to $(k{+}1, k)$ |

This clockwise traversal ensures each element appears exactly once in the 1D ring.

### Perimeter Formula

$$L_k = 2(N - 2k) + 2(M - 2k) - 4 = 2(N + M - 4k) - 4$$

## Modular Rotation

Rotating a ring of length $L$ by $R$ positions counterclockwise is equivalent to shifting the 1D list left by $R \bmod L$ positions.

**Why modular?** $R$ can be up to $10^9$, but the ring length is at most $2(N + M) - 4 \le 1196$. So the effective rotation is always small.

```python
r = R % L
ring = ring[r:] + ring[:r]
```

In C++, `std::rotate` performs this in-place:
```cpp
std::rotate(ring.begin(), ring.begin() + r, ring.end());
```

## CLRS Connection

| Chapter | Relevance |
| :--- | :--- |
| Ch 2 (Getting Started) | Loop invariant: after processing layer $k$, layers $0..k$ are correctly rotated |
| Ch 3 (Growth of Functions) | Total work is $\Theta(NM)$ since each cell is extracted and placed back exactly once |
| Ch 31.3 (Modular Arithmetic) | Modular reduction: $R \bmod L$ maps any rotation count to $[0, L)$ |

## Applications Beyond This Problem

- **Image processing**: Rotating borders of an image
- **Matrix transformations**: Spiralling through a matrix (Spiral Order traversal)
- **Game development**: Rotating puzzle rings (e.g., lock puzzles)
