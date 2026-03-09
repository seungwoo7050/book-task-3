from leader_follower.core import Follower, Leader, LogEntry, ReplicationLog, replicate_once


def test_replication_log_assigns_sequential_offsets():
    log = ReplicationLog()
    assert log.append("put", "a", "1") == 0
    assert log.append("put", "b", "2") == 1


def test_follower_apply_is_idempotent():
    follower = Follower()
    entries = [
        LogEntry(0, "put", "x", "v1"),
        LogEntry(1, "put", "x", "v2"),
    ]
    assert follower.apply(entries) == 2
    assert follower.apply(entries) == 0
    value, ok = follower.get("x")
    assert ok is True
    assert value == "v2"


def test_replicate_once_incremental_and_deletes():
    leader = Leader()
    follower = Follower()

    leader.put("a", "1")
    assert replicate_once(leader, follower) == 1
    assert follower.watermark() == 0

    leader.put("b", "2")
    leader.delete("a")
    assert replicate_once(leader, follower) == 2
    _value, ok = follower.get("a")
    assert ok is False
    value, ok = follower.get("b")
    assert ok is True
    assert value == "2"
