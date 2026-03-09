from pathlib import Path

from wal_recovery import DurableStore, WriteAheadLog


def test_recover_put_records(tmp_path):
    wal_path = tmp_path / "test.wal"
    log = WriteAheadLog(wal_path, False)
    log.open()
    log.append_put("name", "Alice")
    log.append_put("age", "30")
    log.close()
    records = WriteAheadLog(wal_path, False).recover()
    assert len(records) == 2
    assert records[0].record_type == "put"
    assert records[0].key == "name"
    assert records[0].value == "Alice"


def test_recover_delete_records(tmp_path):
    wal_path = tmp_path / "test.wal"
    log = WriteAheadLog(wal_path, False)
    log.open()
    log.append_put("x", "val")
    log.append_delete("x")
    log.close()
    records = WriteAheadLog(wal_path, False).recover()
    assert len(records) == 2
    assert records[1].record_type == "delete"
    assert records[1].key == "x"


def test_recover_many_records(tmp_path):
    wal_path = tmp_path / "test.wal"
    log = WriteAheadLog(wal_path, False)
    log.open()
    for index in range(500):
        log.append_put(f"key:{index}", f"value:{index}")
    log.close()
    records = WriteAheadLog(wal_path, False).recover()
    assert len(records) == 500
    assert records[0].key == "key:0"
    assert records[-1].key == "key:499"


def test_stop_at_corrupted_record(tmp_path):
    wal_path = tmp_path / "test.wal"
    log = WriteAheadLog(wal_path, False)
    log.open()
    log.append_put("good1", "val1")
    log.append_put("good2", "val2")
    log.close()
    with wal_path.open("ab") as handle:
        handle.write(bytes([0xDE, 0xAD, 0xBE, 0xEF, 0x01, 0x00]))
    records = WriteAheadLog(wal_path, False).recover()
    assert len(records) == 2


def test_recover_nonexistent_and_truncated(tmp_path):
    assert WriteAheadLog(tmp_path / "missing.wal", False).recover() == []
    wal_path = tmp_path / "truncated.wal"
    wal_path.write_bytes(bytes([0, 0, 0, 0, 1]))
    assert WriteAheadLog(wal_path, False).recover() == []


def test_store_recovers_from_wal_after_reopen(tmp_path):
    store = DurableStore(tmp_path, 4096, False)
    store.open()
    store.put("persist", "me")
    store.close()
    reopened = DurableStore(tmp_path, 4096, False)
    reopened.open()
    value, found = reopened.get("persist")
    assert found is True
    assert value == "me"


def test_force_flush_rotates_wal(tmp_path):
    store = DurableStore(tmp_path, 4096, False)
    store.open()
    store.put("alpha", "1")
    store.force_flush()
    wal_path = Path(tmp_path) / "active.wal"
    assert wal_path.stat().st_size == 0
    reopened = DurableStore(tmp_path, 4096, False)
    reopened.open()
    value, found = reopened.get("alpha")
    assert found is True
    assert value == "1"
