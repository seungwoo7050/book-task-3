from __future__ import annotations

from tempfile import TemporaryDirectory

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from .core import Cluster, ReplicaGroup


class ValuePayload(BaseModel):
    value: str


def create_app(cluster: Cluster) -> FastAPI:
    app = FastAPI()

    @app.put("/kv/{key}")
    def put_value(key: str, payload: ValuePayload):
        shard_id = cluster.put(key, payload.value)
        return {"key": key, "value": payload.value, "shard_id": shard_id}

    @app.get("/kv/{key}")
    def get_value(key: str):
        value, found, shard_id = cluster.read(key)
        return {"key": key, "value": value if found else None, "found": found, "shard_id": shard_id}

    @app.delete("/kv/{key}")
    def delete_value(key: str):
        shard_id = cluster.delete(key)
        return {"key": key, "shard_id": shard_id}

    return app


def demo() -> None:
    with TemporaryDirectory(prefix="clustered-kv-") as temp_dir:
        cluster = Cluster(
            temp_dir,
            [
                ReplicaGroup("shard-a", "node-1", ["node-2"]),
                ReplicaGroup("shard-b", "node-2", ["node-3"]),
            ],
            64,
        )
        client = TestClient(create_app(cluster))
        client.put("/kv/alpha", json={"value": "1"})
        print(client.get("/kv/alpha").json())
