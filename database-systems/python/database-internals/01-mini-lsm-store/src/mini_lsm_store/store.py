from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory


@dataclass(slots=True)
class SSTable:
    path: Path
    index: dict[str, str | None] | None = None

    @classmethod
    def file_name(cls, data_dir: Path, sequence: int) -> Path:
        return data_dir / f"{sequence:06d}.sst"

    def write(self, records: list[tuple[str, str | None]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            for key, value in records:
                handle.write(json.dumps({"key": key, "value": value}) + "\n")
        self.index = {key: value for key, value in records}

    def load(self) -> None:
        index: dict[str, str | None] = {}
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                entry = json.loads(line)
                index[entry["key"]] = entry["value"]
        self.index = index

    def get(self, key: str) -> tuple[str | None, bool]:
        if self.index is None:
            self.load()
        assert self.index is not None
        if key not in self.index:
            return None, False
        return self.index[key], True


class MiniLSMStore:
    def __init__(self, data_dir: str | Path, memtable_size_threshold: int = 64 * 1024) -> None:
        self.data_dir = Path(data_dir)
        self.memtable_size_threshold = memtable_size_threshold or 64 * 1024
        self.memtable: dict[str, str | None] = {}
        self.immutable_memtable: dict[str, str | None] | None = None
        self.sstables: list[SSTable] = []
        self._next_sequence = 1
        self._byte_size = 0

    def open(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.sstables = []
        sequences: list[int] = []
        for path in sorted(self.data_dir.glob("*.sst")):
            table = SSTable(path)
            table.load()
            self.sstables.append(table)
            sequences.append(int(path.stem))
        self.sstables.reverse()
        if sequences:
            self._next_sequence = max(sequences) + 1

    def put(self, key: str, value: str) -> None:
        self._replace_memtable_value(key, value)
        self._maybe_flush()

    def delete(self, key: str) -> None:
        self._replace_memtable_value(key, None)
        self._maybe_flush()

    def get(self, key: str) -> tuple[str | None, bool]:
        if key in self.memtable:
            return self.memtable[key], True
        if self.immutable_memtable is not None and key in self.immutable_memtable:
            return self.immutable_memtable[key], True
        for table in self.sstables:
            value, found = table.get(key)
            if found:
                return value, True
        return None, False

    def force_flush(self) -> None:
        if not self.memtable:
            return
        self.immutable_memtable = dict(self.memtable)
        self.memtable.clear()
        self._byte_size = 0
        records = sorted(self.immutable_memtable.items())
        table = SSTable(SSTable.file_name(self.data_dir, self._next_sequence))
        self._next_sequence += 1
        table.write(records)
        self.sstables.insert(0, table)
        self.immutable_memtable = None

    def close(self) -> None:
        self.force_flush()

    def _maybe_flush(self) -> None:
        if self._byte_size >= self.memtable_size_threshold:
            self.force_flush()

    def _replace_memtable_value(self, key: str, value: str | None) -> None:
        previous = self.memtable.get(key, ...)
        if previous is not ...:
            self._byte_size -= len(key) + (len(previous) if previous is not None else 0)
        self.memtable[key] = value
        self._byte_size += len(key) + (len(value) if value is not None else 0)


def demo() -> None:
    with TemporaryDirectory(prefix="mini-lsm-store-") as temp_dir:
        store = MiniLSMStore(temp_dir, 32)
        store.open()
        store.put("alpha", "1")
        store.put("beta", "2")
        store.force_flush()
        store.put("alpha", "3")
        value, found = store.get("alpha")
        print({"key": "alpha", "found": found, "value": value, "sstables": len(store.sstables)})
