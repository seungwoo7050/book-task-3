from __future__ import annotations

import bisect
import hashlib
from dataclasses import dataclass


def hash_value(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")


@dataclass(slots=True, order=True)
class RingEntry:
    hash_value: int
    node_id: str


class Ring:
    def __init__(self, virtual_nodes: int = 150) -> None:
        self.virtual_nodes = virtual_nodes or 150
        self.ring: list[RingEntry] = []
        self._nodes: set[str] = set()

    def add_node(self, node_id: str) -> None:
        if node_id in self._nodes:
            return
        self._nodes.add(node_id)
        for index in range(self.virtual_nodes):
            entry = RingEntry(hash_value(f"{node_id}#v{index}"), node_id)
            bisect.insort(self.ring, entry)

    def remove_node(self, node_id: str) -> None:
        self._nodes.discard(node_id)
        self.ring = [entry for entry in self.ring if entry.node_id != node_id]

    def nodes(self) -> list[str]:
        return sorted(self._nodes)

    def node_for_key(self, key: str) -> tuple[str, bool]:
        if not self.ring:
            return "", False
        target = hash_value(key)
        hashes = [entry.hash_value for entry in self.ring]
        index = bisect.bisect_left(hashes, target)
        if index == len(self.ring):
            index = 0
        return self.ring[index].node_id, True

    def assignments(self, keys: list[str]) -> dict[str, str]:
        result = {}
        for key in keys:
            node_id, ok = self.node_for_key(key)
            if ok:
                result[key] = node_id
        return result

    def moved_keys(self, keys: list[str], previous: dict[str, str]) -> int:
        current = self.assignments(keys)
        return sum(1 for key in keys if previous.get(key) and previous[key] != current.get(key))


class Router:
    def __init__(self, ring: Ring) -> None:
        self.ring = ring

    def route(self, key: str) -> tuple[str, bool]:
        return self.ring.node_for_key(key)

    def route_batch(self, keys: list[str]) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = {}
        for key in keys:
            node_id, ok = self.ring.node_for_key(key)
            if ok:
                grouped.setdefault(node_id, []).append(key)
        return grouped


def demo() -> None:
    ring = Ring(100)
    ring.add_node("node-a")
    ring.add_node("node-b")
    router = Router(ring)
    print(router.route_batch(["k1", "k2", "k3", "k4"]))
