from __future__ import annotations

import bisect
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


def hash_value(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode("utf-8")).digest()[:8], "big")


@dataclass(slots=True)
class Operation:
    offset: int
    op_type: str
    key: str
    value: str | None = None


class DiskStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.data: dict[str, str] = {}
        self.log: list[Operation] = []
        self._load()

    def _load(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        self.data = {}
        self.log = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line:
                continue
            payload = json.loads(line)
            op = Operation(payload["offset"], payload["op_type"], payload["key"], payload.get("value"))
            self._apply_in_memory(op)
            self.log.append(op)

    def append_put(self, key: str, value: str) -> Operation:
        op = Operation(len(self.log), "put", key, value)
        self.apply(op)
        return op

    def append_delete(self, key: str) -> Operation:
        op = Operation(len(self.log), "delete", key)
        self.apply(op)
        return op

    def apply(self, op: Operation) -> None:
        if op.offset < len(self.log):
            return
        if op.offset != len(self.log):
            raise ValueError(f"store: non-sequential offset {op.offset}")
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(op)) + "\n")
        self._apply_in_memory(op)
        self.log.append(op)

    def entries_from(self, offset: int) -> list[Operation]:
        return list(self.log[max(offset, 0) :])

    def watermark(self) -> int:
        return len(self.log) - 1

    def get(self, key: str) -> tuple[str, bool]:
        return self.data.get(key, ""), key in self.data

    def reload(self) -> None:
        self._load()

    def _apply_in_memory(self, op: Operation) -> None:
        if op.op_type == "put" and op.value is not None:
            self.data[op.key] = op.value
        if op.op_type == "delete":
            self.data.pop(op.key, None)


@dataclass(slots=True)
class ReplicaGroup:
    shard_id: str
    leader: str
    followers: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Node:
    node_id: str
    stores: dict[str, DiskStore] = field(default_factory=dict)


@dataclass(order=True, slots=True)
class RingEntry:
    hash_value: int
    shard_id: str


class ShardRing:
    def __init__(self, virtual_nodes: int = 64) -> None:
        self.virtual_nodes = virtual_nodes or 64
        self.ring: list[RingEntry] = []

    def add_shard(self, shard_id: str) -> None:
        for index in range(self.virtual_nodes):
            bisect.insort(self.ring, RingEntry(hash_value(f"{shard_id}#v{index}"), shard_id))

    def shard_for_key(self, key: str) -> str:
        target = hash_value(key)
        hashes = [entry.hash_value for entry in self.ring]
        index = bisect.bisect_left(hashes, target)
        if index == len(self.ring):
            index = 0
        return self.ring[index].shard_id


class Cluster:
    def __init__(self, data_dir: str | Path, groups: list[ReplicaGroup], virtual_nodes: int = 64) -> None:
        self.data_dir = Path(data_dir)
        self.router = ShardRing(virtual_nodes)
        self.groups = {group.shard_id: group for group in groups}
        self.nodes: dict[str, Node] = {}
        self.auto_replicate = True
        for group in groups:
            self.router.add_shard(group.shard_id)
            for node_id in [group.leader, *group.followers]:
                node = self.nodes.setdefault(node_id, Node(node_id))
                node.stores[group.shard_id] = DiskStore(self.data_dir / node_id / f"{group.shard_id}.log")

    def set_auto_replicate(self, enabled: bool) -> None:
        self.auto_replicate = enabled

    def route_shard(self, key: str) -> str:
        return self.router.shard_for_key(key)

    def group(self, shard_id: str) -> ReplicaGroup:
        return self.groups[shard_id]

    def put(self, key: str, value: str) -> str:
        shard_id = self.route_shard(key)
        group = self.groups[shard_id]
        self.nodes[group.leader].stores[shard_id].append_put(key, value)
        if self.auto_replicate:
            for follower_id in group.followers:
                self.sync_follower(shard_id, follower_id)
        return shard_id

    def delete(self, key: str) -> str:
        shard_id = self.route_shard(key)
        group = self.groups[shard_id]
        self.nodes[group.leader].stores[shard_id].append_delete(key)
        if self.auto_replicate:
            for follower_id in group.followers:
                self.sync_follower(shard_id, follower_id)
        return shard_id

    def sync_follower(self, shard_id: str, follower_id: str) -> int:
        group = self.groups[shard_id]
        leader_store = self.nodes[group.leader].stores[shard_id]
        follower_store = self.nodes[follower_id].stores[shard_id]
        entries = leader_store.entries_from(follower_store.watermark() + 1)
        applied = 0
        for entry in entries:
            follower_store.apply(entry)
            applied += 1
        return applied

    def read(self, key: str) -> tuple[str, bool, str]:
        shard_id = self.route_shard(key)
        group = self.groups[shard_id]
        value, ok = self.nodes[group.leader].stores[shard_id].get(key)
        return value, ok, shard_id

    def read_from_node(self, node_id: str, key: str) -> tuple[str, bool]:
        shard_id = self.route_shard(key)
        node = self.nodes[node_id]
        if shard_id not in node.stores:
            raise ValueError(f"node {node_id} is not replica for shard {shard_id}")
        return node.stores[shard_id].get(key)

    def restart_node(self, node_id: str) -> None:
        node = self.nodes[node_id]
        for store in node.stores.values():
            store.reload()
