# Distance-Vector Routing — Problem Specification

## 안내

이 문서는 제공 과제 사양을 source-close하게 보존하기 위해 원문 중심으로 유지한다.
공개용 문제 요약과 학습 맥락은 상위 `README.md`를 먼저 참고한다.


## Objective

Implement a distributed distance-vector routing algorithm. Each node in a network independently computes its routing table by exchanging distance vectors with its immediate neighbors, converging to the globally optimal shortest paths.

## Requirements

### Functional Requirements

1. **Node Initialization**
   - Each node reads its link costs to direct neighbors from a topology file
   - Initialize distance vector: cost 0 to self, link cost to neighbors, infinity to all others

2. **Distance Vector Exchange**
   - Each node sends its distance vector to all direct neighbors
   - When a node receives a DV from a neighbor, it runs the Bellman-Ford update:
     $D_x(y) = \min_v\{c(x,v) + D_v(y)\}$ for all destinations $y$
   - If the distance vector changes, notify all neighbors

3. **Convergence**
   - The algorithm terminates when no node's distance vector changes after a round
   - Print the final routing table for each node

4. **Link Cost Changes** (bonus)
   - Support changing a link cost during execution
   - Observe re-convergence
   - Optionally implement **poisoned reverse** to mitigate count-to-infinity

### Topology File Format

```json
{
  "nodes": ["x", "y", "z"],
  "edges": [
    {"from": "x", "to": "y", "cost": 2},
    {"from": "x", "to": "z", "cost": 7},
    {"from": "y", "to": "z", "cost": 1}
  ]
}
```

### Expected Output

```
=== Iteration 0 (Initial) ===
Node x: {x: 0, y: 2, z: 7}
Node y: {x: 2, y: 0, z: 1}
Node z: {x: 7, y: 1, z: 0}

=== Iteration 1 ===
Node x: {x: 0, y: 2, z: 3}  (updated z: min(7, 2+1)=3 via y)
Node y: {x: 2, y: 0, z: 1}  (no change)
Node z: {x: 3, y: 1, z: 0}  (updated x: min(7, 1+2)=3 via y)

=== Converged after 2 iterations ===
Final Routing Tables:
  Node x: to y cost 2 via y | to z cost 3 via y
  Node y: to x cost 2 via x | to z cost 1 via z
  Node z: to x cost 3 via y | to y cost 1 via y
```

## Constraints

- Python 3 standard library only
- Must be a distributed algorithm (each node computes independently)
- Nodes only know their own link costs and received distance vectors
- Must handle arbitrary topologies (not just 3 nodes)

## Input / Environment

- Topology file: `data/topology.json`
- Skeleton code: `code/dv_skeleton.py`
- Test script: `script/test_routing.sh`

## Evaluation Criteria

| Criterion | Description |
| :--- | :--- |
| **Bellman-Ford** | Correctly implements the DV update equation |
| **Convergence** | Algorithm converges to correct shortest paths |
| **Distributed** | Each node operates independently with local info |
| **Output** | Clear routing tables with next-hop info |
| **Link Change** | Handles topology changes (bonus) |
| **Code Quality** | Clean, well-documented code |
