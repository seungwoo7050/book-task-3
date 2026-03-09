from __future__ import annotations

import hashlib
import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

TOMBSTONE_MARKER = 0xFFFFFFFF
FOOTER_MAGIC = b"SIF1"


def _hash_value(key: str, seed: int) -> int:
    payload = f"{seed}:{key}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def encode_record(key: str, value: str | None) -> bytes:
    key_bytes = key.encode()
    value_bytes = b"" if value is None else value.encode()
    value_length = TOMBSTONE_MARKER if value is None else len(value_bytes)
    return struct.pack(">II", len(key_bytes), value_length) + key_bytes + value_bytes


def decode_record(buffer: bytes, offset: int) -> tuple[tuple[str, str | None], int]:
    if len(buffer) < offset + 8:
        raise ValueError("serializer: not enough bytes for header")
    key_length, value_length = struct.unpack(">II", buffer[offset : offset + 8])
    actual_value_length = 0 if value_length == TOMBSTONE_MARKER else value_length
    total_length = 8 + key_length + actual_value_length
    if len(buffer) < offset + total_length:
        raise ValueError(f"serializer: truncated record at offset {offset}")
    key_start = offset + 8
    key_end = key_start + key_length
    value = None if value_length == TOMBSTONE_MARKER else buffer[key_end : key_end + actual_value_length].decode()
    return (buffer[key_start:key_end].decode(), value), total_length


@dataclass(slots=True)
class LookupStats:
    bloom_rejected: bool = False
    bytes_read: int = 0
    block_range: tuple[int, int] = (0, 0)


class BloomFilter:
    def __init__(self, expected_items: int, false_positive_rate: float = 0.01) -> None:
        expected_items = max(expected_items, 1)
        if not 0 < false_positive_rate < 1:
            false_positive_rate = 0.01
        bit_count = math.ceil(-(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2))
        hash_functions = max(1, round((bit_count / expected_items) * math.log(2)))
        self.bit_count = bit_count
        self.hash_functions = hash_functions
        self.bits = bytearray(math.ceil(bit_count / 8))

    def add(self, key: str) -> None:
        for position in self.positions(key):
            self.bits[position // 8] |= 1 << (position % 8)

    def might_contain(self, key: str) -> bool:
        for position in self.positions(key):
            if self.bits[position // 8] & (1 << (position % 8)) == 0:
                return False
        return True

    def serialize(self) -> bytes:
        return struct.pack(">II", self.bit_count, self.hash_functions) + bytes(self.bits)

    @classmethod
    def deserialize(cls, buffer: bytes) -> "BloomFilter":
        if len(buffer) < 8:
            raise ValueError("bloomfilter: buffer too small")
        bit_count, hash_functions = struct.unpack(">II", buffer[:8])
        if bit_count == 0 or hash_functions == 0:
            raise ValueError("bloomfilter: malformed header")
        instance = cls(1)
        instance.bit_count = bit_count
        instance.hash_functions = hash_functions
        instance.bits = bytearray(buffer[8:])
        return instance

    def positions(self, key: str) -> list[int]:
        h1 = _hash_value(key, 0)
        h2 = _hash_value(key, 42)
        return [int((h1 + index * h2) % self.bit_count) for index in range(self.hash_functions)]


@dataclass(slots=True)
class IndexEntry:
    key: str
    offset: int


class SparseIndex:
    def __init__(self, block_size: int = 16) -> None:
        self.block_size = block_size or 16
        self.entries: list[IndexEntry] = []

    def build(self, entries: list[IndexEntry]) -> None:
        self.entries = [entry for index, entry in enumerate(entries) if index % self.block_size == 0]

    def find_block(self, key: str, data_size: int) -> tuple[tuple[int, int], bool]:
        if not self.entries or key < self.entries[0].key:
            return (0, 0), False
        low = 0
        high = len(self.entries) - 1
        block = 0
        while low <= high:
            mid = (low + high) // 2
            if self.entries[mid].key <= key:
                block = mid
                low = mid + 1
            else:
                high = mid - 1
        start = self.entries[block].offset
        end = data_size if block + 1 >= len(self.entries) else self.entries[block + 1].offset
        return (start, end), True

    def serialize(self) -> bytes:
        payload = [{"key": entry.key, "offset": entry.offset} for entry in self.entries]
        return json.dumps(payload).encode("utf-8")

    @classmethod
    def deserialize(cls, buffer: bytes, block_size: int) -> "SparseIndex":
        data = json.loads(buffer.decode("utf-8"))
        instance = cls(block_size)
        instance.entries = [IndexEntry(entry["key"], entry["offset"]) for entry in data]
        return instance


class SSTable:
    def __init__(self, path: str | Path, block_size: int = 16) -> None:
        self.path = Path(path)
        self.block_size = block_size or 16
        self.data_size = 0
        self.bloom_offset = 0
        self.bloom_size = 0
        self.index_offset = 0
        self.index_size = 0
        self.filter: BloomFilter | None = None
        self.index: SparseIndex | None = None

    def write(self, records: list[tuple[str, str | None]]) -> None:
        if records != sorted(records, key=lambda item: item[0]):
            raise ValueError("sstable: records must be sorted")
        data_section = bytearray()
        offsets: list[IndexEntry] = []
        bloom = BloomFilter(len(records) + 1, 0.01)
        offset = 0
        for key, value in records:
            bloom.add(key)
            encoded = encode_record(key, value)
            offsets.append(IndexEntry(key, offset))
            data_section.extend(encoded)
            offset += len(encoded)

        index = SparseIndex(self.block_size)
        index.build(offsets)
        index_bytes = index.serialize()
        bloom_bytes = bloom.serialize()

        self.data_size = len(data_section)
        self.bloom_offset = self.data_size
        self.bloom_size = len(bloom_bytes)
        self.index_offset = self.bloom_offset + self.bloom_size
        self.index_size = len(index_bytes)
        self.filter = bloom
        self.index = index

        footer = FOOTER_MAGIC + struct.pack(">QQQQI", self.bloom_offset, self.bloom_size, self.index_offset, self.index_size, self.block_size)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_bytes(bytes(data_section) + bloom_bytes + index_bytes + footer)

    def load(self) -> None:
        buffer = self.path.read_bytes()
        if len(buffer) < 40:
            raise ValueError("sstable: file too small")
        footer = buffer[-40:]
        if footer[:4] != FOOTER_MAGIC:
            raise ValueError("sstable: invalid footer magic")
        (
            self.bloom_offset,
            self.bloom_size,
            self.index_offset,
            self.index_size,
            self.block_size,
        ) = struct.unpack(">QQQQI", footer[4:])
        self.data_size = self.bloom_offset
        self.filter = BloomFilter.deserialize(buffer[self.bloom_offset : self.bloom_offset + self.bloom_size])
        self.index = SparseIndex.deserialize(buffer[self.index_offset : self.index_offset + self.index_size], self.block_size)

    def get(self, key: str) -> tuple[str | None, bool]:
        value, ok, _, _ = self.get_with_stats(key)
        return value, ok

    def get_with_stats(self, key: str) -> tuple[str | None, bool, LookupStats, None]:
        if self.filter is None or self.index is None:
            self.load()
        assert self.filter is not None
        assert self.index is not None
        if not self.filter.might_contain(key):
            return None, False, LookupStats(bloom_rejected=True), None
        block_range, ok = self.index.find_block(key, self.data_size)
        if not ok:
            return None, False, LookupStats(), None

        start, end = block_range
        with self.path.open("rb") as handle:
            handle.seek(start)
            block = handle.read(end - start)
        stats = LookupStats(bytes_read=len(block), block_range=block_range)
        offset = 0
        while offset < len(block):
            (record_key, value), bytes_read = decode_record(block, offset)
            if record_key == key:
                return value, True, stats, None
            if record_key > key:
                return None, False, stats, None
            offset += bytes_read
        return None, False, stats, None


def demo() -> None:
    with TemporaryDirectory(prefix="index-filter-") as temp_dir:
        table = SSTable(Path(temp_dir) / "table.sst", 8)
        records = [(f"k{index:03d}", f"value-k{index:03d}") for index in range(32)]
        table.write(records)
        value, found, stats, _ = table.get_with_stats("k023")
        print({"found": found, "value": value, "bytes_read": stats.bytes_read})
