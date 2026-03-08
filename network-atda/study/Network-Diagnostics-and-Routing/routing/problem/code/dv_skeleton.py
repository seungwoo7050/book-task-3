"""
Distance-Vector Routing — Skeleton Code

Simulates the distributed Bellman-Ford distance-vector routing algorithm.

Usage:
    python3 dv_skeleton.py <topology.json>
"""

import copy
import json
import sys

INF = float("inf")


def load_topology(filepath: str) -> tuple[list[str], dict[str, dict[str, int]]]:
    """Load network topology from a JSON file.

    Args:
        filepath: Path to the topology JSON file.

    Returns:
        A tuple of (node_list, adjacency_dict).
        adjacency_dict maps each node to {neighbor: cost}.
    """
    with open(filepath) as f:
        data = json.load(f)

    nodes = data["nodes"]
    adj: dict[str, dict[str, int]] = {n: {} for n in nodes}

    for edge in data["edges"]:
        u, v, cost = edge["from"], edge["to"], edge["cost"]
        adj[u][v] = cost
        adj[v][u] = cost  # Undirected

    return nodes, adj


class DVNode:
    """A node running the distance-vector algorithm.

    Attributes:
        name: The node's identifier.
        neighbors: Dict mapping neighbor name to link cost.
        all_nodes: List of all node names in the network.
        distance_vector: Dict mapping destination to best-known cost.
        next_hop: Dict mapping destination to next-hop node.
        neighbor_dvs: Dict mapping neighbor to their last-advertised DV.
    """

    def __init__(
        self,
        name: str,
        neighbors: dict[str, int],
        all_nodes: list[str],
    ):
        self.name = name
        self.neighbors = neighbors
        self.all_nodes = all_nodes

        # Initialize distance vector
        self.distance_vector: dict[str, float] = {}
        self.next_hop: dict[str, str | None] = {}
        self.neighbor_dvs: dict[str, dict[str, float]] = {}

        # TODO: Initialize the distance vector:
        #   - Cost 0 to self
        #   - Link cost to each neighbor
        #   - INF to all other nodes
        #   Set next_hop accordingly.

    def receive_dv(self, sender: str, dv: dict[str, float]) -> bool:
        """Process a distance vector received from a neighbor.

        Args:
            sender: The neighbor that sent this DV.
            dv: The neighbor's distance vector.

        Returns:
            True if this node's DV changed, False otherwise.
        """
        # TODO:
        #   1. Store the neighbor's DV
        #   2. For each destination y, recompute:
        #      D_x(y) = min over all neighbors v of { c(x,v) + D_v(y) }
        #   3. Update next_hop accordingly
        #   4. Return True if any entry changed
        return False  # Replace

    def get_dv(self) -> dict[str, float]:
        """Return a copy of this node's current distance vector."""
        return copy.deepcopy(self.distance_vector)

    def format_routing_table(self) -> str:
        """Return a formatted string of the routing table."""
        entries = []
        for dest in sorted(self.all_nodes):
            if dest == self.name:
                continue
            cost = self.distance_vector.get(dest, INF)
            hop = self.next_hop.get(dest, "-")
            cost_str = str(cost) if cost != INF else "INF"
            entries.append(f"to {dest} cost {cost_str} via {hop}")
        return f"Node {self.name}: " + " | ".join(entries)


def simulate(topology_file: str) -> None:
    """Run the DV routing simulation.

    Args:
        topology_file: Path to the topology JSON file.
    """
    nodes, adj = load_topology(topology_file)

    # TODO:
    #   1. Create DVNode objects for each node
    #   2. Print initial distance vectors (Iteration 0)
    #   3. Loop:
    #      a. Each node sends its DV to all neighbors
    #      b. Each node processes received DVs
    #      c. Print updated distance vectors
    #      d. If no changes occurred, declare convergence and break
    #   4. Print final routing tables

    print("[TODO] Implement the simulate() function")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dv_skeleton.py <topology.json>")
        sys.exit(1)

    simulate(sys.argv[1])
