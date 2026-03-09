from __future__ import annotations

import time

from starlette.websockets import WebSocketDisconnect


def test_websocket_notification_delivery_and_presence(client) -> None:
    with client.websocket_connect("/api/v1/realtime/ws/notifications/alice?token=alice") as websocket:
        heartbeat = client.post("/api/v1/realtime/presence/heartbeat", json={"user_id": "alice"})
        assert heartbeat.status_code == 200
        assert client.get("/api/v1/realtime/presence/alice").json()["online"] is True

        delivered = client.post(
            "/api/v1/realtime/notifications",
            json={"user_id": "alice", "message": "build complete"},
        )
        assert delivered.status_code == 200
        assert websocket.receive_json() == {"message": "build complete"}


def test_invalid_token_disconnects_and_presence_expires(client) -> None:
    try:
        with client.websocket_connect("/api/v1/realtime/ws/notifications/bob?token=wrong"):
            raise AssertionError("connection should not stay open")
    except WebSocketDisconnect:
        pass

    heartbeat = client.post("/api/v1/realtime/presence/heartbeat", json={"user_id": "carol"})
    assert heartbeat.status_code == 200
    time.sleep(1.1)
    assert client.get("/api/v1/realtime/presence/carol").json()["online"] is False
