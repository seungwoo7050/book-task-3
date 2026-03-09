from pathlib import Path

from buffer_pool import BufferPool, LRUCache


def test_lru_basic_operations():
    cache = LRUCache(3)
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("missing") is None
    cache.put("a", 2)
    assert cache.get("a") == 2
    assert cache.size() == 1


def test_lru_eviction_and_promotion():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    evicted = cache.put("d", 4)
    assert evicted is not None
    assert evicted.key == "a"
    cache.get("b")
    evicted = cache.put("e", 5)
    assert evicted is not None
    assert evicted.key == "c"


def test_lru_ordering_and_delete():
    cache = LRUCache(3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.keys() == ["c", "b", "a"]
    cache.get("a")
    assert cache.keys() == ["a", "c", "b"]
    assert cache.delete("a") is True
    assert cache.delete("missing") is False


def test_fetch_page_from_disk(tmp_path):
    data_file = seed_pages(tmp_path)
    pool = BufferPool(4, 64)
    page = pool.fetch_page(f"{data_file}:0")
    assert page.pin_count == 1
    assert bytes(page.data[:6]) == b"page-0"


def test_return_cached_page(tmp_path):
    data_file = seed_pages(tmp_path)
    pool = BufferPool(4, 64)
    page1 = pool.fetch_page(f"{data_file}:2")
    pool.unpin_page(f"{data_file}:2", False)
    page2 = pool.fetch_page(f"{data_file}:2")
    assert page1 is page2


def test_track_dirty_pages(tmp_path):
    data_file = seed_pages(tmp_path)
    pool = BufferPool(4, 64)
    page = pool.fetch_page(f"{data_file}:0")
    page.data[:8] = b"modified"
    pool.unpin_page(f"{data_file}:0", True)
    assert page.dirty is True


def test_eviction_after_unpin(tmp_path):
    data_file = seed_pages(tmp_path)
    pool = BufferPool(2, 64)
    page0 = pool.fetch_page(f"{data_file}:0")
    assert bytes(page0.data[:6]) == b"page-0"
    pool.unpin_page(f"{data_file}:0", False)
    page1 = pool.fetch_page(f"{data_file}:1")
    assert bytes(page1.data[:6]) == b"page-1"
    pool.unpin_page(f"{data_file}:1", False)
    page2 = pool.fetch_page(f"{data_file}:2")
    assert bytes(page2.data[:6]) == b"page-2"


def seed_pages(tmp_path) -> Path:
    data_file = Path(tmp_path) / "data.db"
    pages = bytearray()
    for index in range(10):
        buffer = bytearray(64)
        payload = f"page-{index}".encode()
        buffer[: len(payload)] = payload
        pages.extend(buffer)
    data_file.write_bytes(pages)
    return data_file
