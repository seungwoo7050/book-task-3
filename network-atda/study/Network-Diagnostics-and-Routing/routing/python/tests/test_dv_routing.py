"""
Distance-Vector Routing — Unit Tests

Usage:
    python3 -m pytest test_dv_routing.py -v
"""

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dv_routing import DVNode, load_topology, INF


def _make_topo_file(nodes, edges):
    """Create a temporary topology JSON file."""
    data = {"nodes": nodes, "edges": edges}
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    )
    json.dump(data, tmp)
    tmp.close()
    return tmp.name


class TestLoadTopology:
    """Tests for topology loading."""

    def test_3node(self):
        path = _make_topo_file(
            ["x", "y", "z"],
            [
                {"from": "x", "to": "y", "cost": 2},
                {"from": "x", "to": "z", "cost": 7},
                {"from": "y", "to": "z", "cost": 1},
            ],
        )
        nodes, adj = load_topology(path)
        os.unlink(path)

        assert sorted(nodes) == ["x", "y", "z"]
        assert adj["x"]["y"] == 2
        assert adj["y"]["x"] == 2  # Undirected
        assert adj["x"]["z"] == 7
        assert adj["y"]["z"] == 1

    def test_no_self_links(self):
        path = _make_topo_file(
            ["a", "b"],
            [{"from": "a", "to": "b", "cost": 3}],
        )
        _, adj = load_topology(path)
        os.unlink(path)

        assert "a" not in adj["a"]
        assert "b" not in adj["b"]


class TestDVNode:
    """Tests for the DVNode class."""

    def _make_triangle(self):
        """Create the x-y-z triangle network nodes."""
        nodes = ["x", "y", "z"]
        adj_x = {"y": 2, "z": 7}
        adj_y = {"x": 2, "z": 1}
        adj_z = {"x": 7, "y": 1}
        return (
            DVNode("x", adj_x, nodes),
            DVNode("y", adj_y, nodes),
            DVNode("z", adj_z, nodes),
        )

    def test_initial_dv(self):
        x, y, z = self._make_triangle()
        assert x.distance_vector["x"] == 0
        assert x.distance_vector["y"] == 2
        assert x.distance_vector["z"] == 7

    def test_convergence(self):
        """After exchanging DVs, x's cost to z should be 3 (via y)."""
        x, y, z = self._make_triangle()

        # Simulate a round
        dvs = {"x": x.get_dv(), "y": y.get_dv(), "z": z.get_dv()}

        x.receive_dv("y", dvs["y"])
        x.receive_dv("z", dvs["z"])

        assert x.distance_vector["z"] == 3
        assert x.next_hop["z"] == "y"

    def test_no_change_returns_false(self):
        """If no update occurs, receive_dv should return False."""
        x, y, z = self._make_triangle()

        dvs = {"x": x.get_dv(), "y": y.get_dv(), "z": z.get_dv()}
        x.receive_dv("y", dvs["y"])
        x.receive_dv("z", dvs["z"])

        # Second round with same DVs — no change expected
        dvs2 = {"x": x.get_dv(), "y": y.get_dv(), "z": z.get_dv()}
        changed = x.receive_dv("y", dvs2["y"])
        assert not changed

    def test_5node_topology(self):
        """Test on a 5-node topology."""
        nodes = ["a", "b", "c", "d", "e"]
        adj = {
            "a": {"b": 1, "c": 5},
            "b": {"a": 1, "c": 2, "d": 4},
            "c": {"a": 5, "b": 2, "d": 1, "e": 3},
            "d": {"b": 4, "c": 1, "e": 1},
            "e": {"c": 3, "d": 1},
        }
        dv_nodes = {n: DVNode(n, adj[n], nodes) for n in nodes}

        # Run until convergence
        for _ in range(20):
            msgs = {n: dv_nodes[n].get_dv() for n in nodes}
            any_changed = False
            for n in nodes:
                for nbr in adj[n]:
                    if dv_nodes[n].receive_dv(nbr, msgs[nbr]):
                        any_changed = True
            if not any_changed:
                break

        # a→e: a→b(1)→c(2)→d(1)→e(1) = 5
        assert dv_nodes["a"].distance_vector["e"] == 5
        # a→d: a→b(1)→c(2)→d(1) = 4
        assert dv_nodes["a"].distance_vector["d"] == 4
