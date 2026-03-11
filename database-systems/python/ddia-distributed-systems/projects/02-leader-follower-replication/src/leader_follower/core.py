from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LogEntry:
    offset: int
    operation: str
    key: str
    value: str | None


class ReplicationLog:
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []

    def append(self, operation: str, key: str, value: str | None) -> int:
        offset = len(self.entries)
        self.entries.append(LogEntry(offset, operation, key, value))
        return offset

    def from_offset(self, offset: int) -> list[LogEntry]:
        return list(self.entries[max(offset, 0) :])

    def latest_offset(self) -> int:
        return len(self.entries) - 1


class Leader:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.log = ReplicationLog()

    def put(self, key: str, value: str) -> int:
        self.store[key] = value
        return self.log.append("put", key, value)

    def delete(self, key: str) -> int:
        self.store.pop(key, None)
        return self.log.append("delete", key, None)

    def get(self, key: str) -> tuple[str, bool]:
        return self.store.get(key, ""), key in self.store

    def log_from(self, offset: int) -> list[LogEntry]:
        return self.log.from_offset(offset)

    def latest_offset(self) -> int:
        return self.log.latest_offset()


class Follower:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.last_applied_offset = -1

    def apply(self, entries: list[LogEntry]) -> int:
        applied = 0
        for entry in entries:
            if entry.offset <= self.last_applied_offset:
                continue
            if entry.operation == "put" and entry.value is not None:
                self.store[entry.key] = entry.value
            if entry.operation == "delete":
                self.store.pop(entry.key, None)
            self.last_applied_offset = entry.offset
            applied += 1
        return applied

    def get(self, key: str) -> tuple[str, bool]:
        return self.store.get(key, ""), key in self.store

    def watermark(self) -> int:
        return self.last_applied_offset


def replicate_once(leader: Leader, follower: Follower) -> int:
    entries = leader.log_from(follower.watermark() + 1)
    return follower.apply(entries)


def demo() -> None:
    leader = Leader()
    follower = Follower()
    leader.put("alpha", "1")
    applied = replicate_once(leader, follower)
    print({"applied": applied, "value": follower.get("alpha")[0]})
