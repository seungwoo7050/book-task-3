from mini_lsm_store import MiniLSMStore


def test_put_and_get(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("greeting", "hello")
    value, found = store.get("greeting")
    assert found is True
    assert value == "hello"


def test_missing_key(tmp_path):
    store = open_store(tmp_path, 1024)
    value, found = store.get("nope")
    assert found is False
    assert value is None


def test_update(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("k", "v1")
    store.put("k", "v2")
    value, found = store.get("k")
    assert found is True
    assert value == "v2"


def test_delete(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("k", "v")
    store.delete("k")
    value, found = store.get("k")
    assert found is True
    assert value is None


def test_flush_creates_sstable(tmp_path):
    store = open_store(tmp_path, 256)
    for index in range(50):
        store.put(f"key-{index:03d}", "x" * 30)
    assert store.sstables


def test_read_after_force_flush(tmp_path):
    store = open_store(tmp_path, 1024)
    for index in range(50):
        store.put(f"k{index:03d}", f"v{index}")
    store.force_flush()
    value, found = store.get("k025")
    assert found is True
    assert value == "v25"


def test_memtable_wins_over_sstable(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("key", "old")
    store.force_flush()
    store.put("key", "new")
    value, found = store.get("key")
    assert found is True
    assert value == "new"


def test_tombstone_across_levels(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("key", "value")
    store.force_flush()
    store.delete("key")
    value, found = store.get("key")
    assert found is True
    assert value is None


def test_persistence_after_reopen(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("persist", "me")
    store.close()

    reopened = MiniLSMStore(tmp_path, 1024)
    reopened.open()
    value, found = reopened.get("persist")
    assert found is True
    assert value == "me"


def open_store(tmp_path, threshold: int) -> MiniLSMStore:
    store = MiniLSMStore(tmp_path, threshold)
    store.open()
    return store
