from fastapi.testclient import TestClient

from clustered_kv import Cluster, ReplicaGroup, create_app


def test_write_routes_to_leader_and_replicates(tmp_path):
    cluster = new_cluster(tmp_path)
    shard_id = cluster.put("alpha", "1")
    group = cluster.group(shard_id)

    value, ok = cluster.read_from_node(group.leader, "alpha")
    assert ok is True
    assert value == "1"

    value, ok = cluster.read_from_node(group.followers[0], "alpha")
    assert ok is True
    assert value == "1"


def test_follower_catch_up_and_delete(tmp_path):
    cluster = new_cluster(tmp_path)
    cluster.set_auto_replicate(False)
    shard_id = cluster.put("beta", "2")
    group = cluster.group(shard_id)

    _value, ok = cluster.read_from_node(group.followers[0], "beta")
    assert ok is False

    applied = cluster.sync_follower(shard_id, group.followers[0])
    assert applied == 1
    value, ok = cluster.read_from_node(group.followers[0], "beta")
    assert ok is True
    assert value == "2"

    cluster.set_auto_replicate(True)
    cluster.delete("beta")
    _value, ok = cluster.read_from_node(group.followers[0], "beta")
    assert ok is False


def test_restart_node_loads_from_disk(tmp_path):
    cluster = new_cluster(tmp_path)
    shard_id = cluster.put("gamma", "3")
    group = cluster.group(shard_id)
    follower = group.followers[0]

    cluster.restart_node(follower)
    value, ok = cluster.read_from_node(follower, "gamma")
    assert ok is True
    assert value == "3"


def test_fastapi_round_trip(tmp_path):
    cluster = new_cluster(tmp_path)
    client = TestClient(create_app(cluster))

    response = client.put("/kv/alpha", json={"value": "1"})
    assert response.status_code == 200
    shard_id = response.json()["shard_id"]
    assert shard_id in {"shard-a", "shard-b"}

    response = client.get("/kv/alpha")
    assert response.status_code == 200
    assert response.json()["found"] is True
    assert response.json()["value"] == "1"

    response = client.delete("/kv/alpha")
    assert response.status_code == 200

    response = client.get("/kv/alpha")
    assert response.json()["found"] is False


def new_cluster(tmp_path) -> Cluster:
    return Cluster(
        tmp_path,
        [
            ReplicaGroup("shard-a", "node-1", ["node-2"]),
            ReplicaGroup("shard-b", "node-2", ["node-3"]),
        ],
        64,
    )
