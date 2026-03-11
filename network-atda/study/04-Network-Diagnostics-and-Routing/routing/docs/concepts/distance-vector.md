# Distance-Vector Algorithm

## Overview

The **Distance-Vector (DV) algorithm** is a distributed routing protocol where each node:

1. Maintains a **distance vector** — its estimated least cost to every destination
2. Periodically sends its DV to its **direct neighbors**
3. Upon receiving a neighbor's DV, **updates** its own using the Bellman-Ford equation
4. Repeats until **convergence** (no more changes)

## Algorithm Pseudocode

```
For each node x:

  Initialization:
    D_x(x) = 0
    D_x(y) = c(x, y)   if y is a neighbor
    D_x(y) = INF        otherwise
    Send D_x to all neighbors

  Loop:
    Wait for a DV update from any neighbor v
    For each destination y:
      D_x(y) = min over all neighbors v { c(x,v) + D_v(y) }
    If D_x changed:
      Send D_x to all neighbors

  Until no more changes
```

## Detailed Example: 3-Node Network

```
Network: x ---2--- y ---1--- z
         └────────7────────┘
```

### Iteration 0 (Initialization)

| Node | D(x) | D(y) | D(z) |
| :--- | :--- | :--- | :--- |
| x | 0 | 2 | 7 |
| y | 2 | 0 | 1 |
| z | 7 | 1 | 0 |

### Iteration 1

Node **x** receives DVs from y and z:
- $D_x(z) = \min(c(x,z) + D_z(z),\; c(x,y) + D_y(z)) = \min(7+0,\; 2+1) = 3$
- Updated: $D_x(z): 7 → 3$ (via y)

Node **z** receives DVs from x and y:
- $D_z(x) = \min(c(z,x) + D_x(x),\; c(z,y) + D_y(x)) = \min(7+0,\; 1+2) = 3$
- Updated: $D_z(x): 7 → 3$ (via y)

| Node | D(x) | D(y) | D(z) |
| :--- | :--- | :--- | :--- |
| x | 0 | 2 | **3** |
| y | 2 | 0 | 1 |
| z | **3** | 1 | 0 |

### Iteration 2

No changes → **Converged!**

## Properties

| Property | Description |
| :--- | :--- |
| **Distributed** | Each node computes using only local info + neighbor DVs |
| **Iterative** | Updates propagate hop-by-hop through the network |
| **Asynchronous** | Nodes don't need to update simultaneously |
| **Self-terminating** | Stops when no DV changes occur |

## Synchronous Simulation

In our implementation, we simulate synchronous rounds:

```python
while True:
    changed = False
    # Phase 1: Collect all DVs
    messages = {}
    for node in nodes:
        messages[node.name] = node.get_dv()

    # Phase 2: Deliver DVs to neighbors
    for node in nodes:
        for neighbor_name in node.neighbors:
            if node.receive_dv(neighbor_name, messages[neighbor_name]):
                changed = True

    if not changed:
        break  # Converged
```

## Comparison with Link-State Routing

| Feature | Distance-Vector | Link-State |
| :--- | :--- | :--- |
| Algorithm | Bellman-Ford | Dijkstra |
| Information shared | Distance vector to neighbors | Full topology to all |
| Knowledge | Only neighbor costs + DVs | Complete network graph |
| Convergence speed | Slower | Faster |
| Message complexity | O(N) per node per round | O(N²) total (flooding) |
| Scalability | Good for small networks | Better for large networks |
