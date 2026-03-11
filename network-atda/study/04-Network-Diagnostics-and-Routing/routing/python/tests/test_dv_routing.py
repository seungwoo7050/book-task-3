"""
Distance-Vector Routing unit test.

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
    """임시 topology JSON file을 만든다."""
    data = {"nodes": nodes, "edges": edges}
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    )
    json.dump(data, tmp)
    tmp.close()
    return tmp.name


class TestLoadTopology:
    """topology loading 동작을 확인한다."""

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
        assert adj["y"]["x"] == 2  # 무방향 그래프라 반대 방향도 동일해야 한다.
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
    """DVNode 클래스의 상태 갱신을 검증한다."""

    def _make_triangle(self):
        """x-y-z 삼각형 topology의 node를 만든다."""
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
        """DV를 교환하면 x에서 z까지 cost가 3(via y)로 수렴해야 한다."""
        x, y, z = self._make_triangle()

        # 한 round 동안 DV를 교환한다고 가정한다.
        dvs = {"x": x.get_dv(), "y": y.get_dv(), "z": z.get_dv()}

        x.receive_dv("y", dvs["y"])
        x.receive_dv("z", dvs["z"])

        assert x.distance_vector["z"] == 3
        assert x.next_hop["z"] == "y"

    def test_no_change_returns_false(self):
        """더 이상 갱신이 없으면 `receive_dv`는 False를 반환해야 한다."""
        x, y, z = self._make_triangle()

        dvs = {"x": x.get_dv(), "y": y.get_dv(), "z": z.get_dv()}
        x.receive_dv("y", dvs["y"])
        x.receive_dv("z", dvs["z"])

        # 같은 DV를 한 번 더 받아도 더 이상 바뀌지 않아야 한다.
        dvs2 = {"x": x.get_dv(), "y": y.get_dv(), "z": z.get_dv()}
        changed = x.receive_dv("y", dvs2["y"])
        assert not changed

    def test_5node_topology(self):
        """5-node topology에서도 기대한 최단 cost가 나와야 한다."""
        nodes = ["a", "b", "c", "d", "e"]
        adj = {
            "a": {"b": 1, "c": 5},
            "b": {"a": 1, "c": 2, "d": 4},
            "c": {"a": 5, "b": 2, "d": 1, "e": 3},
            "d": {"b": 4, "c": 1, "e": 1},
            "e": {"c": 3, "d": 1},
        }
        dv_nodes = {n: DVNode(n, adj[n], nodes) for n in nodes}

        # 충분한 round를 돌며 수렴할 때까지 반복한다.
        for _ in range(20):
            msgs = {n: dv_nodes[n].get_dv() for n in nodes}
            any_changed = False
            for n in nodes:
                for nbr in adj[n]:
                    if dv_nodes[n].receive_dv(nbr, msgs[nbr]):
                        any_changed = True
            if not any_changed:
                break

        # 경로 a→e: a→b(1)→c(2)→d(1)→e(1) = 5
        assert dv_nodes["a"].distance_vector["e"] == 5
        # 경로 a→d: a→b(1)→c(2)→d(1) = 4
        assert dv_nodes["a"].distance_vector["d"] == 4
