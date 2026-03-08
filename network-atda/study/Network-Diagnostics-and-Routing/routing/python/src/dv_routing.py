"""
Distance-Vector Routing — Complete Solution

Simulates the distributed Bellman-Ford distance-vector routing algorithm.

Usage:
    python3 dv_routing.py <topology.json>
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
        adjacency_dict maps node -> {neighbor: cost}.
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

        for node in all_nodes:
            if node == name:
                self.distance_vector[node] = 0
                self.next_hop[node] = None
            elif node in neighbors:
                self.distance_vector[node] = neighbors[node]
                self.next_hop[node] = node
            else:
                self.distance_vector[node] = INF
                self.next_hop[node] = None

    def receive_dv(self, sender: str, dv: dict[str, float]) -> bool:
        """Process a distance vector received from a neighbor.

        Args:
            sender: The neighbor that sent this DV.
            dv: The neighbor's distance vector.

        Returns:
            True if this node's DV changed, False otherwise.
        """
        self.neighbor_dvs[sender] = copy.deepcopy(dv)
        changed = False

        for dest in self.all_nodes:
            if dest == self.name:
                continue

            # Bellman-Ford: D_x(y) = min over v { c(x,v) + D_v(y) }
            best_cost = self.distance_vector[dest]
            best_hop = self.next_hop[dest]

            for v, link_cost in self.neighbors.items():
                if v in self.neighbor_dvs:
                    cost_via_v = link_cost + self.neighbor_dvs[v].get(dest, INF)
                elif v == dest:
                    cost_via_v = link_cost
                else:
                    continue

                if cost_via_v < best_cost:
                    best_cost = cost_via_v
                    best_hop = v

            if best_cost != self.distance_vector[dest]:
                self.distance_vector[dest] = best_cost
                self.next_hop[dest] = best_hop
                changed = True

        return changed

    def get_dv(self) -> dict[str, float]:
        """Return a copy of this node's current distance vector."""
        return copy.deepcopy(self.distance_vector)

    def format_dv(self) -> str:
        """Return a formatted string of the distance vector."""
        entries = []
        for dest in sorted(self.all_nodes):
            cost = self.distance_vector[dest]
            cost_str = str(int(cost)) if cost != INF else "INF"
            entries.append(f"{dest}: {cost_str}")
        return f"Node {self.name}: {{{', '.join(entries)}}}"

    def format_routing_table(self) -> str:
        """Return a formatted string of the routing table."""
        entries = []
        for dest in sorted(self.all_nodes):
            if dest == self.name:
                continue
            cost = self.distance_vector[dest]
            hop = self.next_hop.get(dest, "-")
            cost_str = str(int(cost)) if cost != INF else "INF"
            entries.append(f"to {dest} cost {cost_str} via {hop}")
        return f"  Node {self.name}: " + " | ".join(entries)


def simulate(topology_file: str) -> None:
    """Run the DV routing simulation.

    Args:
        topology_file: Path to the topology JSON file.
    """
    nodes, adj = load_topology(topology_file)

    # Create nodes
    dv_nodes: dict[str, DVNode] = {}
    for name in nodes:
        dv_nodes[name] = DVNode(name, adj[name], nodes)

    # Print initial state
    print("=== Iteration 0 (Initial) ===")
    for name in sorted(nodes):
        print(dv_nodes[name].format_dv())
    print()

    max_iterations = len(nodes) * 10  # Safety limit

    for iteration in range(1, max_iterations + 1):
        # Phase 1: Collect all DVs
        messages: dict[str, dict[str, float]] = {}
        for name, node in dv_nodes.items():
            messages[name] = node.get_dv()

        # Phase 2: Deliver DVs to neighbors and update
        any_changed = False
        for name, node in dv_nodes.items():
            for neighbor_name in node.neighbors:
                if node.receive_dv(neighbor_name, messages[neighbor_name]):
                    any_changed = True

        print(f"=== Iteration {iteration} ===")
        for name in sorted(nodes):
            print(dv_nodes[name].format_dv())
        print()

        if not any_changed:
            print(f"=== Converged after {iteration} iterations ===\n")
            break
    else:
        print(f"WARNING: Did not converge within {max_iterations} iterations\n")

    # Print final routing tables
    print("Final Routing Tables:")
    for name in sorted(nodes):
        print(dv_nodes[name].format_routing_table())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dv_routing.py <topology.json>")
        sys.exit(1)

    simulate(sys.argv[1])
