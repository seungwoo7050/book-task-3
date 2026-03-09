from shard_routing import Ring, Router


def test_empty_and_single_node_routing():
    ring = Ring(50)
    assert ring.node_for_key("key") == ("", False)
    ring.add_node("node-a")
    assert ring.node_for_key("key") == ("node-a", True)


def test_distribution_and_rebalance():
    ring = Ring(150)
    ring.add_node("node-a")
    ring.add_node("node-b")
    ring.add_node("node-c")

    keys = [f"key-{index}" for index in range(3000)]
    counts = {"node-a": 0, "node-b": 0, "node-c": 0}
    for key in keys:
        node_id, _ = ring.node_for_key(key)
        counts[node_id] += 1
    for node_id in counts:
        share = counts[node_id] / 3000
        assert 0.2 < share < 0.5

    movement_keys = keys[:1000]
    before = ring.assignments(movement_keys)
    ring.add_node("node-d")
    moved = ring.moved_keys(movement_keys, before)
    assert 50 < moved < 500

    ring.remove_node("node-b")
    for index in range(100):
        node_id, _ = ring.node_for_key(f"key-{index}")
        assert node_id != "node-b"


def test_batch_routing():
    ring = Ring(100)
    ring.add_node("node-a")
    ring.add_node("node-b")
    router = Router(ring)
    grouped = router.route_batch(["k1", "k2", "k3", "k4", "k5"])
    assert sum(len(keys) for keys in grouped.values()) == 5
