# workspace-backend-v2-msa 개발 타임라인

## 2026-03-10
### Session 1

- 목표: v1을 보면 "서비스가 4개로 늘어나면 어떤 것이 복잡해지는가?"가 궁금했다. 처음엔 "인증만 identity-service로 빼고, 나머지는 workspace-service 하나에 그대로 두면 되지 않나?"라고 생각했다.
- 진행: `contracts/README.md`를 읽었다. gateway, identity-service, workspace-service, notification-service 네 개로 나뉘어 있다. notification은 왜 따로 빼야 했나? workspace-service에 같이 두면 안 됐나?
- 이슈: v1에서는 `create_comment`와 `drain_notifications`가 같은 서비스 안에 있었다. v2에서 comment는 workspace-service가 쓰고, drain은 gateway가 notification-service를 호출해야 한다. 서비스 경계를 나누면 "코드 위치"가 달라질 뿐만 아니라, 실패 모드도 달라진다.
- 판단: v1에서 "하나의 성공"이었던 comment+알림이 v2에서는 (1) comment 저장 성공, (2) workspace-service outbox 적재 성공, (3) notification-service consume 성공, (4) gateway pub/sub → websocket 전달 성공으로 4단계가 된다. 각 단계마다 실패할 수 있다.

CLI:

```bash
$ cd capstone/workspace-backend-v2-msa/fastapi
$ make install
$ make test  # service unit tests
```

### Session 2

- 목표: system test를 돌리려면 Compose로 모든 서비스를 올려야 한다. `docker compose up --build -d`를 실행했다.
- 이슈: 빌드가 중간에 멈췄다. `python:3.12-slim` 베이스 이미지를 pull 하는 단계에서 응답이 없었다. 처음엔 "네트워크 문제인가?" 싶었다.

```bash
$ docker build --progress=plain -t workspace-v2-identity-fresh ./services/identity-service
# 빌드 단계에서 python:3.12-slim 레이어를 pull하려다 멈춤
$ docker pull python:3.12-slim
# 마찬가지로 응답 없음
```

- 진행: Docker Desktop을 재시작했다. 그래도 fresh build는 안 됐다. 검증 보고서에 "Docker Desktop 이미지 손상"이라고 기록했다. 대신 이전에 로컬에 쌓아 둔 prebuilt image를 복구해서 `--no-build`로 올렸다.

```bash
$ docker compose -p workspace-backend-v2-msa-dd63448c -f compose.yaml up -d --no-build
```

- 판단: fresh build 경로는 이 날 안정적으로 성공했다고 기록할 수 없다. 하지만 서비스 unit test와 prebuilt image 기반 end-to-end 검증은 완료했다.

### Session 3

- 목표: Compose가 올라간 상태에서 system test 흐름을 확인한다.
- 진행: `test_system.py`를 처음 돌렸을 때 gateway 포트(8015)로 연결은 됐지만, `/api/v1/auth/register` 응답이 503이었다. gateway의 ready 체크가 identity-service까지 포함하는데, identity-service가 아직 ready가 아니었다.
- 조치: `wait_for` 헬퍼로 gateway ready를 기다린 뒤 테스트를 진행했다.
- 진행: 전체 흐름이 이어졌다.

```python
owner = httpx.Client(base_url="http://127.0.0.1:8015", timeout=10.0)
collaborator = httpx.Client(base_url="http://127.0.0.1:8015", timeout=10.0)
# gateway 하나의 base URL만 사용
```

v1에서 `TestClient(owner.app)`으로 같은 앱 인스턴스를 공유하던 것이, v2에서는 같은 gateway 포트를 가리키는 두 개의 httpx.Client로 바뀌었다. 외부에서 보면 같은 "하나의 주소"다.

- 이슈: H~K에서 배웠던 `uvicorn app.main:app` Dockerfile CMD가 v2에서도 처음엔 그렇게 돼 있었다. 그런데 컨테이너 안에서 `uvicorn`이 PATH에 없는 경우가 생겼다. `python -m uvicorn app.main:app`으로 바꾸고 나서 해결됐다. H부터 K, v2 전체를 같은 패턴으로 맞췄다.

### Session 4

- 목표: notification-service 장애 후 recovery까지 확인. v1에서는 단일 서비스 안에서 `drain_notifications`가 그냥 websocket push를 했다. v2에서는 drain이 notification-service HTTP 호출이다.
- 진행: system test에서 notification-service를 `docker compose stop`으로 내리고, drain이 503을 돌려보내는지 확인했다.

```python
failed_drain = owner.post("/api/v1/platform/notifications/drain")
assert failed_drain.status_code == 503
```

- 재기동 후 notification-service 포트(8117) ready를 직접 폴링하고, recovery drain 후 websocket 메시지를 수신했다.

```python
wait_for("http://127.0.0.1:8117/api/v1/health/ready")
recovery_drain = owner.post("/api/v1/platform/notifications/drain")
assert recovery_drain.status_code == 200
assert "Second comment after consumer outage." in websocket.recv(timeout=20)
```

- 판단: v1에서 "코드 한 줄 실패"였던 게, v2에서는 "서비스 불가 503"으로 바뀐다. 복잡도가 커지는 부분이다. 대신 notification-service만 재시작하면 되고, workspace-service는 계속 comment 저장을 받는다. 이게 MSA에서 isolation이 실제로 주는 이득이다.

CLI:

```bash
$ make test
$ python -m pytest tests/test_system.py -q
```

```
1 passed
```
