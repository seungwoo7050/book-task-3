from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Version:
    value: object
    tx_id: int
    deleted: bool


class VersionStore:
    def __init__(self) -> None:
        self.store: dict[str, list[Version]] = {}

    def append(self, key: str, value: object, tx_id: int, deleted: bool) -> None:
        chain = self.store.setdefault(key, [])
        index = 0
        while index < len(chain) and chain[index].tx_id > tx_id:
            index += 1
        chain.insert(index, Version(value, tx_id, deleted))

    def get_visible(self, key: str, snapshot: int, committed: dict[int, bool]) -> Version | None:
        for version in self.store.get(key, []):
            if version.tx_id <= snapshot and committed.get(version.tx_id, False):
                return Version(version.value, version.tx_id, version.deleted)
        return None

    def remove_by_tx_id(self, key: str, tx_id: int) -> None:
        filtered = [version for version in self.store.get(key, []) if version.tx_id != tx_id]
        if filtered:
            self.store[key] = filtered
        else:
            self.store.pop(key, None)

    def gc(self, min_snapshot: int) -> None:
        for key, chain in list(self.store.items()):
            recent = [version for version in chain if version.tx_id >= min_snapshot]
            old = [version for version in chain if version.tx_id < min_snapshot]
            if old:
                recent.append(old[0])
            if recent:
                self.store[key] = recent
            else:
                del self.store[key]


@dataclass(slots=True)
class Transaction:
    snapshot: int
    status: str
    write_set: set[str] = field(default_factory=set)


class TransactionManager:
    def __init__(self) -> None:
        self.next_tx_id = 1
        self.version_store = VersionStore()
        self.transactions: dict[int, Transaction] = {}
        self.committed: dict[int, bool] = {}

    def begin(self) -> int:
        tx_id = self.next_tx_id
        self.next_tx_id += 1
        snapshot = max(self.committed, default=0)
        self.transactions[tx_id] = Transaction(snapshot=snapshot, status="active")
        return tx_id

    def read(self, tx_id: int, key: str):
        tx = self._active_tx(tx_id)
        if key in tx.write_set:
            for version in self.version_store.store.get(key, []):
                if version.tx_id == tx_id:
                    return None if version.deleted else version.value
        version = self.version_store.get_visible(key, tx.snapshot, self.committed)
        if version is None or version.deleted:
            return None
        return version.value

    def write(self, tx_id: int, key: str, value) -> None:
        tx = self._active_tx(tx_id)
        self.version_store.append(key, value, tx_id, False)
        tx.write_set.add(key)

    def delete(self, tx_id: int, key: str) -> None:
        tx = self._active_tx(tx_id)
        self.version_store.append(key, None, tx_id, True)
        tx.write_set.add(key)

    def commit(self, tx_id: int) -> None:
        tx = self._active_tx(tx_id)
        for key in tx.write_set:
            for version in self.version_store.store.get(key, []):
                if version.tx_id > tx.snapshot and version.tx_id != tx_id and self.committed.get(version.tx_id, False):
                    self._abort_internal(tx_id, tx)
                    raise ValueError(f'write-write conflict on key "{key}"')
        tx.status = "committed"
        self.committed[tx_id] = True

    def abort(self, tx_id: int) -> None:
        self._abort_internal(tx_id, self._active_tx(tx_id))

    def gc(self) -> None:
        min_snapshot = self.next_tx_id
        for tx in self.transactions.values():
            if tx.status == "active" and tx.snapshot < min_snapshot:
                min_snapshot = tx.snapshot
        self.version_store.gc(min_snapshot)

    def _active_tx(self, tx_id: int) -> Transaction:
        tx = self.transactions.get(tx_id)
        if tx is None:
            raise ValueError(f"unknown transaction {tx_id}")
        if tx.status != "active":
            raise ValueError(f"transaction {tx_id} is {tx.status}")
        return tx

    def _abort_internal(self, tx_id: int, tx: Transaction) -> None:
        for key in tx.write_set:
            self.version_store.remove_by_tx_id(key, tx_id)
        tx.status = "aborted"


def demo() -> None:
    manager = TransactionManager()
    tx_id = manager.begin()
    manager.write(tx_id, "x", 10)
    print({"tx": tx_id, "read_your_own_write": manager.read(tx_id, "x")})
