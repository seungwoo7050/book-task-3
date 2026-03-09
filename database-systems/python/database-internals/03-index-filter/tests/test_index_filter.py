from index_filter import BloomFilter, SSTable, SparseIndex
from index_filter.table import IndexEntry


def test_bloom_filter_has_no_false_negatives():
    bloom = BloomFilter(512, 0.01)
    keys = [fmt_key(index) for index in range(512)]
    for key in keys:
        bloom.add(key)
    for key in keys:
        assert bloom.might_contain(key) is True


def test_bloom_filter_false_positive_rate_is_bounded():
    bloom = BloomFilter(1000, 0.01)
    for index in range(1000):
        bloom.add(f"present-{fmt_key(index)}")
    false_positives = 0
    total = 5000
    for index in range(total):
        if bloom.might_contain(f"absent-{fmt_key(index)}"):
            false_positives += 1
    assert false_positives / total <= 0.03


def test_sparse_index_finds_expected_block():
    index = SparseIndex(8)
    entries = [IndexEntry(fmt_key(value), value * 20) for value in range(32)]
    index.build(entries)
    block, ok = index.find_block(fmt_key(17), 640)
    assert ok is True
    assert block == (320, 480)


def test_sstable_bloom_reject_and_bounded_scan(tmp_path):
    table = SSTable(tmp_path / "index.sst", 8)
    records = [(fmt_key(index), f"value-{fmt_key(index)}") for index in range(64)]
    table.write(records)

    value, ok, stats, _ = table.get_with_stats("missing-key")
    assert ok is False
    assert value is None
    assert stats.bloom_rejected is True
    assert stats.bytes_read == 0

    value, ok, stats, _ = table.get_with_stats(fmt_key(23))
    assert ok is True
    assert value == f"value-{fmt_key(23)}"
    assert 0 < stats.bytes_read < table.data_size


def fmt_key(value: int) -> str:
    return f"k{value:03d}"
