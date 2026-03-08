from __future__ import annotations


def test_healthcheck(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_creates_conversation_and_turn(client):
    response = client.post(
        "/api/chat",
        json={"user_message": "프리미엄 요금제 해지하면 위약금 있나요?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["conversation_id"]
    assert payload["turn_id"]
    assert isinstance(payload["retrieved_doc_ids"], list)

    list_response = client.get("/api/conversations")
    assert list_response.status_code == 200
    items = list_response.json()["items"]
    assert len(items) >= 1

    detail_response = client.get(f"/api/conversations/{payload['conversation_id']}")
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert len(detail["turns"]) == 1


def test_chat_appends_turn_in_same_conversation(client):
    first = client.post("/api/chat", json={"user_message": "베이직 요금 얼마야?"}).json()
    second = client.post(
        "/api/chat",
        json={"conversation_id": first["conversation_id"], "user_message": "해지 절차도 알려줘"},
    ).json()

    assert first["conversation_id"] == second["conversation_id"]

    detail = client.get(f"/api/conversations/{first['conversation_id']}").json()
    assert len(detail["turns"]) == 2
    assert detail["turns"][0]["turn_index"] == 1
    assert detail["turns"][1]["turn_index"] == 2
