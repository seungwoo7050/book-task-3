# Bellman-Ford Equation

## The Equation

The **Bellman-Ford equation** (also called the distance-vector equation) defines the minimum-cost path from node $x$ to node $y$:

$$D_x(y) = \min_v \{ c(x,v) + D_v(y) \}$$

Where:
- $D_x(y)$: Least cost from $x$ to $y$
- $c(x,v)$: Cost of the direct link from $x$ to neighbor $v$
- $D_v(y)$: Neighbor $v$'s least cost to $y$
- The minimum is taken over all neighbors $v$ of $x$

## Intuition

To find the cheapest path from $x$ to $y$:
1. Consider every neighbor $v$ of $x$
2. For each $v$, the cost is: (link cost $x → v$) + (cheapest cost $v → y$)
3. Pick the neighbor that minimizes the total cost

## Example

Consider a triangle network:

```
     x ---2--- y
      \       /
       7     1
        \   /
          z
```

To compute $D_x(z)$:

| Via neighbor $v$ | $c(x,v) + D_v(z)$ |
| :--- | :--- |
| $v = y$ | $c(x,y) + D_y(z) = 2 + 1 = 3$ |
| $v = z$ | $c(x,z) + D_z(z) = 7 + 0 = 7$ |

$$D_x(z) = \min(3, 7) = 3 \text{ (via } y\text{)}$$

## Properties

1. **Optimal Substructure**: Shortest paths contain shortest sub-paths
2. **Distributed**: Each node only needs its neighbors' distance vectors
3. **Iterative**: Repeated application converges to the correct answer
4. **Convergence**: Guaranteed for graphs with no negative-cost cycles

## Relationship to Shortest Paths

The Bellman-Ford equation is equivalent to the classic **Bellman-Ford algorithm** for finding single-source shortest paths in a weighted graph:

```
Initialize:
  D[source] = 0
  D[v] = INF for all other v

Repeat (|V| - 1) times:
  For each edge (u, v) with cost w:
    if D[u] + w < D[v]:
      D[v] = D[u] + w
```

In the distributed version, each node runs this independently using only local information.
