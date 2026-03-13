# I-event-integration-lab: 동기 API 뒤에 outbox와 idempotent consumer를 붙여 eventual consistency를 드러내기

이 글은 `labs/I-event-integration-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/I-event-integration-lab/fastapi/compose.yaml::__compose__`, `labs/I-event-integration-lab/fastapi/tests/test_system.py::test_outbox_and_idempotent_consumer_flow`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

I 랩은 H 랩보다 더 많은 서비스를 자랑하려는 프로젝트가 아니다. 오히려 focus는 더 뚜렷하다. problem/README.md는 comment 저장이 outbox에 기록되고, relay 후 notification-service가 consume하며, 같은 consume를 두 번 돌려도 결과가 중복되지 않아야 한다고 말한다. 즉 이 랩의 주인공은 API 호출보다 이벤트 전달 경로다.

## 1. 서비스 통합을 동기 API 대신 이벤트 전달 문제로 보기
처음에는 무엇을 늦게 끝내도 되는지부터 정해야 했다. README는 workspace outbox 적재, Redis Streams relay, notification consume와 dedupe를 한 답으로 묶는다. docs/README.md도 'outbox가 왜 여전히 필요한가'와 'idempotent consumer는 어떤 실패를 흡수하는가'를 먼저 묻는다. 이 프로젝트가 알림 기능보다 전달 경계에 초점을 둔다는 뜻이다.

## 2. compose runtime을 workspace + notification + redis로 좁히기
실제 runtime도 그 경계를 따라간다. compose에는 workspace-service, notification-service, redis만 올라오고, identity나 gateway는 일부러 빠진다. 그래서 이 랩은 MSA 전체가 아니라 producer와 consumer가 stream을 사이에 두고 만나는 최소 모델로 읽어야 한다.

```yaml
services:
  workspace-service:
    build:
      context: ./services/workspace-service
    env_file:
      - .env
    environment:
      DATABASE_URL: ${WORKSPACE_DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      REDIS_STREAM_NAME: ${REDIS_STREAM_NAME}
      SECRET_KEY: ${SECRET_KEY}
      TOKEN_ISSUER: ${TOKEN_ISSUER}
    depends_on:
      redis:
        condition: service_healthy
    ports:
      - "8012:8000"
    command: >
      sh -c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    volumes:
      - ./services/workspace-service:/app
      - workspace_data:/data
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health/live')\"",
        ]
```

여기서 분명해지는 건 runtime이 workspace-service, notification-service, redis 셋으로만 구성된다는 점이다.

## 3. system test로 relay와 dedupe를 고정하기
system test가 특히 좋다. comment를 생성한 직후 pending_outbox가 1인지 확인하고, relay를 한 번 수행한 뒤 notification-service consume를 두 번 호출한다. 첫 번째는 processed == 1, 두 번째는 processed == 0이어야 한다. 마지막에는 collaborator 알림이 정확히 1건 저장됐는지 본다. 이 흐름 하나로 eventual consistency와 dedupe가 동시에 설명된다.

```python
def test_outbox_and_idempotent_consumer_flow() -> None:
    with compose_stack():
        owner_token = _token("00000000-0000-4000-8000-000000000011", "owner", "owner@example.com")
        collaborator_token = _token("00000000-0000-4000-8000-000000000012", "collab", "collab@example.com")
        workspace = httpx.Client(base_url="http://127.0.0.1:8012/api/v1", timeout=10.0)
        notifications = httpx.Client(base_url="http://127.0.0.1:8112/api/v1", timeout=10.0)

        created_workspace = workspace.post(
            "/internal/workspaces",
            json={"name": "Alpha"},
            headers={"Authorization": f"Bearer {owner_token}"},
        ).json()
```

테스트는 comment 저장, relay, 두 번 consume, notification dedupe가 한 흐름으로 이어짐을 고정한다.

## 4. 2026-03-10 재검증으로 eventual consistency surface를 닫기
보고서 기준으로 2026-03-10에 lint, service unit test, system test, smoke가 다시 통과했다. 이 기록 덕분에 I 랩은 단순 개념 설명이 아니라, 실제로 다시 돌려 볼 수 있는 producer-consumer 실험실이 된다. 다음 J 랩에서 gateway를 얹어도 이벤트 경계 설명이 흐려지지 않는 이유가 바로 여기에 있다.

```bash
make lint
make test
make smoke
docker compose up --build
```

2026-03-10에 lint, service unit test, system test, smoke가 통과했다. 이 랩의 독립성은 gateway 없이도 producer-consumer 경로가 설명되고 실행된다는 데 있다.

## 정리
I 랩이 남기는 핵심은 '댓글 생성 성공'과 '알림 생성 완료'를 같은 의미로 보지 않는 태도다. 그 차이를 outbox와 dedupe로 고정했기 때문에, 이후 gateway나 운영성을 붙여도 어떤 지연과 실패를 허용하는지 더 분명하게 설명할 수 있다.
