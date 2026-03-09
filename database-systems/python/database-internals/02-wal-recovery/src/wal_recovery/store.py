from __future__ import annotations

import json
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

TOMBSTONE_MARKER = 0xFFFFFFFF
OP_PUT = 0x01
OP_DELETE = 0x02


@dataclass(slots=True)
class WALRecord:
    record_type: str
    key: str
    value: str | None = None


class WriteAheadLog:
    def __init__(self, path: str | Path, fsync_enabled: bool = False) -> None:
        self.path = Path(path)
        self.fsync_enabled = fsync_enabled
        self._handle = None

    def open(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("ab")

    def append_put(self, key: str, value: str) -> None:
        self._append_record(OP_PUT, key, value)

    def append_delete(self, key: str) -> None:
        self._append_record(OP_DELETE, key, None)

    def recover(self) -> list[WALRecord]:
        if not self.path.exists():
            return []
        buffer = self.path.read_bytes()
        records: list[WALRecord] = []
        offset = 0
        while offset < len(buffer):
            if offset + 13 > len(buffer):
                break
            stored_crc = struct.unpack(">I", buffer[offset : offset + 4])[0]
            record_type = buffer[offset + 4]
            key_length = struct.unpack(">I", buffer[offset + 5 : offset + 9])[0]
            value_length = struct.unpack(">I", buffer[offset + 9 : offset + 13])[0]
            actual_value_length = 0 if value_length == TOMBSTONE_MARKER else value_length
            record_size = 13 + key_length + actual_value_length
            if offset + record_size > len(buffer):
                break
            payload = buffer[offset + 4 : offset + record_size]
            if zlib.crc32(payload) & 0xFFFFFFFF != stored_crc:
                break
            key_start = offset + 13
            key_end = key_start + key_length
            key = buffer[key_start:key_end].decode()
            if record_type == OP_DELETE:
                records.append(WALRecord("delete", key))
            else:
                value = buffer[key_end : key_end + actual_value_length].decode()
                records.append(WALRecord("put", key, value))
            offset += record_size
        return records

    def close(self) -> None:
        if self._handle is not None:
            self._handle.close()
            self._handle = None

    def _append_record(self, record_type: int, key: str, value: str | None) -> None:
        if self._handle is None:
            raise RuntimeError("wal: append on closed log")
        key_bytes = key.encode()
        value_bytes = b"" if value is None else value.encode()
        value_length = TOMBSTONE_MARKER if value is None else len(value_bytes)
        header = struct.pack(">BII", record_type, len(key_bytes), value_length)
        payload = header + key_bytes + value_bytes
        record = struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF) + payload
        self._handle.write(record)
        self._handle.flush()


class SSTable:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.index: dict[str, str | None] = {}

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
        self.index = {}
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                entry = json.loads(line)
                self.index[entry["key"]] = entry["value"]

    def get(self, key: str) -> tuple[str | None, bool]:
        if not self.index:
            self.load()
        if key not in self.index:
            return None, False
        return self.index[key], True


class DurableStore:
    def __init__(self, data_dir: str | Path, memtable_size_threshold: int = 64 * 1024, fsync_enabled: bool = False) -> None:
        self.data_dir = Path(data_dir)
        self.memtable_size_threshold = memtable_size_threshold or 64 * 1024
        self.wal_path = self.data_dir / "active.wal"
        self.memtable: dict[str, str | None] = {}
        self.sstables: list[SSTable] = []
        self._next_sequence = 1
        self._byte_size = 0
        self._wal = WriteAheadLog(self.wal_path, fsync_enabled)

    def open(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        sequences: list[int] = []
        self.sstables = []
        for path in sorted(self.data_dir.glob("*.sst")):
            table = SSTable(path)
            table.load()
            self.sstables.append(table)
            sequences.append(int(path.stem))
        self.sstables.reverse()
        if sequences:
            self._next_sequence = max(sequences) + 1

        for record in WriteAheadLog(self.wal_path, False).recover():
            self._replace_memtable_value(record.key, record.value if record.record_type == "put" else None)
        self._wal.open()

    def put(self, key: str, value: str) -> None:
        self._wal.append_put(key, value)
        self._replace_memtable_value(key, value)
        self._maybe_flush()

    def delete(self, key: str) -> None:
        self._wal.append_delete(key)
        self._replace_memtable_value(key, None)
        self._maybe_flush()

    def get(self, key: str) -> tuple[str | None, bool]:
        if key in self.memtable:
            return self.memtable[key], True
        for table in self.sstables:
            value, found = table.get(key)
            if found:
                return value, True
        return None, False

    def force_flush(self) -> None:
        if not self.memtable:
            return
        table = SSTable(SSTable.file_name(self.data_dir, self._next_sequence))
        self._next_sequence += 1
        table.write(sorted(self.memtable.items()))
        self.sstables.insert(0, table)
        self._wal.close()
        if self.wal_path.exists():
            self.wal_path.unlink()
        self.memtable.clear()
        self._byte_size = 0
        self._wal = WriteAheadLog(self.wal_path, self._wal.fsync_enabled)
        self._wal.open()

    def close(self) -> None:
        self._wal.close()

    def _replace_memtable_value(self, key: str, value: str | None) -> None:
        previous = self.memtable.get(key, ...)
        if previous is not ...:
            self._byte_size -= len(key) + (len(previous) if previous is not None else 0)
        self.memtable[key] = value
        self._byte_size += len(key) + (len(value) if value is not None else 0)

    def _maybe_flush(self) -> None:
        if self._byte_size >= self.memtable_size_threshold:
            self.force_flush()


def demo() -> None:
    with TemporaryDirectory(prefix="wal-recovery-") as temp_dir:
        store = DurableStore(temp_dir, 64)
        store.open()
        store.put("alpha", "1")
        store.close()
        reopened = DurableStore(temp_dir, 64)
        reopened.open()
        value, found = reopened.get("alpha")
        print({"recovered": found, "value": value})
