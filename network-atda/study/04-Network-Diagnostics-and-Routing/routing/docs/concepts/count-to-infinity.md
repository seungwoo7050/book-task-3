# Count-to-Infinity Problem

## The Problem

The **count-to-infinity** problem is a well-known failure mode of the distance-vector algorithm. When a link cost increases (or a link goes down), the algorithm can take a very long time to converge, with nodes slowly "counting up" to infinity.

## Example

Consider the simple network:

```
x ---4--- y ---1--- z
```

Converged routing tables:
- $D_y(x) = 4$ (direct)
- $D_z(x) = 5$ (via y)

Now suppose the link cost $c(x,y)$ changes from `4` to `60`:

### What Goes Wrong

1. **y** detects the link cost change: $c(x,y) = 60$
2. **y** recomputes: $D_y(x) = \min(60, c(y,z) + D_z(x)) = \min(60, 1+5) = 6$ (via z)
   - But $D_z(x) = 5$ was computed **through y** — this is already stale!
3. **z** receives y's new DV: $D_z(x) = \min(c(z,y) + D_y(x)) = 1 + 6 = 7$
4. **y** receives z's new DV: $D_y(x) = \min(60, 1 + 7) = 8$
5. This continues: 6, 7, 8, 9, 10, ... until reaching 60

The nodes "count to infinity" (or rather, to the actual new minimum cost), taking many iterations.

## Why It Happens

Node **z** bases its cost on **y**'s old information, and **y** in turn uses **z**'s now-stale value. This **routing loop** causes both nodes to slowly increment their costs.

## Solution 1: Poisoned Reverse

With **poisoned reverse**, if a node **z** routes to **x** through **y**, then z tells y that its cost to x is **infinity**:

```
z's DV to y: {x: INF, ...}    (because z reaches x via y)
z's DV to others: {x: 5, ...}  (actual cost)
```

This prevents y from using z as a path back to x through y itself.

### How It Helps

1. $c(x,y)$ changes to 60
2. **y** receives z's DV with $D_z(x) = \infty$ (poisoned)
3. **y** computes: $D_y(x) = \min(60, 1 + \infty) = 60$ (direct link)
4. **z** receives y's new DV: $D_z(x) = 1 + 60 = 61$
5. Converges immediately without counting

### Limitations

Poisoned reverse **only works for 2-node loops**. For loops involving 3 or more nodes (A→B→C→A), it fails.

## Solution 2: Define Infinity

Set a maximum value (e.g., 16 in RIP) to represent infinity. If a distance reaches this value, the destination is considered unreachable.

## Solution 3: Split Horizon

A simpler version of poisoned reverse: never advertise a route back through the neighbor that is the next hop for that route.

```
If z reaches x via y:
  z does NOT include x in DVs sent to y
```

## Implementation Note

For this assignment, basic DV without poisoned reverse is sufficient. Implementing poisoned reverse is a **bonus** task.

```python
def get_dv_for_neighbor(self, neighbor: str) -> dict[str, float]:
    """Return DV with poisoned reverse applied."""
    dv = copy.deepcopy(self.distance_vector)
    for dest in dv:
        if self.next_hop.get(dest) == neighbor and dest != neighbor:
            dv[dest] = INF  # Poison the route
    return dv
```
