from mvcc_lab import TransactionManager


def test_basic_read_write():
    manager = TransactionManager()
    t1 = manager.begin()
    manager.write(t1, "x", 10)
    assert manager.read(t1, "x") == 10
    manager.commit(t1)

    t2 = manager.begin()
    assert manager.read(t2, "missing") is None
    manager.commit(t2)


def test_snapshot_isolation():
    manager = TransactionManager()
    t1 = manager.begin()
    manager.write(t1, "x", 100)
    manager.commit(t1)

    t2 = manager.begin()
    t3 = manager.begin()
    manager.write(t3, "x", 200)
    manager.commit(t3)
    assert manager.read(t2, "x") == 100
    manager.commit(t2)


def test_latest_committed_value():
    manager = TransactionManager()
    t1 = manager.begin()
    manager.write(t1, "a", "v1")
    manager.commit(t1)

    t2 = manager.begin()
    manager.write(t2, "a", "v2")
    manager.commit(t2)

    t3 = manager.begin()
    assert manager.read(t3, "a") == "v2"
    manager.commit(t3)


def test_write_write_conflict():
    manager = TransactionManager()
    t1 = manager.begin()
    t2 = manager.begin()
    manager.write(t1, "x", "alpha")
    manager.write(t2, "x", "beta")
    manager.commit(t1)
    try:
        manager.commit(t2)
    except ValueError as error:
        assert "write-write conflict" in str(error)
    else:
        raise AssertionError("expected conflict")


def test_different_keys_no_conflict():
    manager = TransactionManager()
    t1 = manager.begin()
    t2 = manager.begin()
    manager.write(t1, "x", 1)
    manager.write(t2, "y", 2)
    manager.commit(t1)
    manager.commit(t2)


def test_abort_and_delete():
    manager = TransactionManager()
    t1 = manager.begin()
    manager.write(t1, "x", "temp")
    manager.abort(t1)

    t2 = manager.begin()
    assert manager.read(t2, "x") is None
    manager.commit(t2)

    t3 = manager.begin()
    manager.write(t3, "x", "hello")
    manager.commit(t3)

    t4 = manager.begin()
    manager.delete(t4, "x")
    manager.commit(t4)

    t5 = manager.begin()
    assert manager.read(t5, "x") is None
    manager.commit(t5)


def test_gc():
    manager = TransactionManager()
    t1 = manager.begin()
    manager.write(t1, "x", "v1")
    manager.commit(t1)

    t2 = manager.begin()
    manager.write(t2, "x", "v2")
    manager.commit(t2)

    t3 = manager.begin()
    manager.write(t3, "x", "v3")
    manager.commit(t3)

    manager.gc()

    t4 = manager.begin()
    assert manager.read(t4, "x") == "v3"
    manager.commit(t4)
    assert len(manager.version_store.store["x"]) <= 2
