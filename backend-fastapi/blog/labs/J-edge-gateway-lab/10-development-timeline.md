# J-edge-gateway-lab 개발 타임라인

## 2026-03-10
### Session 1

- 목표: H에서 서비스를 나누고 I에서 이벤트 통합을 했는데, 클라이언트는 여전히 내부 서비스 포트를 직접 호출해야 한다. "하나의 API 주소"로 쓰려면 gateway가 필요하다. 처음엔 "Nginx reverse proxy를 앞에 두면 끝 아닌가?"라고 생각했다.
- 진행: `problem/README.md`를 읽었다. 단순 reverse proxy가 아니라, cookie와 CSRF를 edge에만 두고, 내부 서비스에는 bearer token과 request id만 전달하는 구조를 요구한다.
- 이슈: 왜 cookie를 gateway에만 둬야 하나? 처음엔 내부 서비스도 cookie를 읽으면 편할 거라 생각했다. 하지만 내부 서비스가 cookie를 직접 다루면, 각 서비스가 cookie 파싱/검증 로직을 중복으로 가져야 한다. gateway에서 cookie를 벗겨 bearer token으로 변환하고, 내부는 bearer만 읽으면 경계가 깔끔해진다.
- 판단: gateway가 맡아야 할 책임을 먼저 정리하기로 했다. (1) public route 유지, (2) cookie → bearer 변환, (3) request id 생성, (4) websocket edge.

CLI:

```bash
$ cd labs/J-edge-gateway-lab/fastapi
$ make install
```

### Session 2

- 목표: gateway에서 내부 서비스로 fan-out할 때 request id를 함께 전달하는 구조를 만든다.
- 진행: H에서 만든 request id middleware를 gateway에 그대로 가져왔다. 그리고 내부 호출 시 `X-Request-ID` 헤더를 붙여 보내는 `_forward` 메서드를 만들었다.

```python
outgoing_headers = {"X-Request-ID": request.state.request_id}
if headers:
    outgoing_headers.update(headers)
with httpx.Client(base_url=self.base_urls[service], timeout=self.settings.request_timeout_seconds) as client:
    response = client.request(method, path, json=json, headers=outgoing_headers)
```

처음엔 httpx를 요청마다 새로 만드는 게 비효율적이라고 생각했다. connection pool을 유지하면 더 좋지만, 이 랩에서는 "request id 전파"라는 패턴을 명확하게 보여 주는 게 우선이다.

- 이슈: gateway → identity-service → workspace-service로 이어지는 호출 체인에서, 마지막 서비스의 응답 헤더에도 같은 request id가 돌아와야 한다. 내부 서비스들도 같은 middleware를 달아야 하나?
- 판단: 그렇다. 내부 서비스도 request id middleware를 달면, 로그에서 하나의 요청 흐름을 전체적으로 추적할 수 있다.

### Session 3

- 목표: system test에서 gateway 하나의 base URL만 사용하면서 전체 협업 흐름을 확인한다.
- 진행: owner local login, collaborator Google login, workspace → invite → accept → project → task → comment → drain → websocket 수신까지 전체를 gateway 포트 하나에서 진행한다.
- 이슈: websocket도 gateway를 통해야 한다. 처음엔 websocket 연결을 내부 서비스에 직접 연결하려 했는데, 그러면 클라이언트가 내부 포트를 알아야 한다.
- 조치: gateway에 websocket route를 추가하고, 내부 notification-service의 pub/sub과 연결했다.

```python
with connect(f"ws://127.0.0.1:8013/api/v1/platform/ws/notifications?access_token={access_token}") as websocket:
    # ... comment 생성 후 drain
    assert "New comment on task" in websocket.recv(timeout=20)
```

### Session 4

- 목표: notification-service 장애 후 recovery drain을 테스트한다.
- 진행: system test에서 `docker compose stop notification-service`로 알림 서비스를 내린 뒤, drain이 503을 돌려보내는지 확인한다.
- 이슈: 처음엔 notification-service가 죽으면 댓글 저장도 실패할 거라 예상했다. 하지만 outbox 패턴 덕분에 댓글 저장은 성공하고, drain만 실패한다.
- 검증: 재기동 후 ready를 기다리고, recovery drain으로 밀린 알림이 전달되는 것까지 확인.

```python
subprocess.run(
    ["docker", "compose", "-p", project_name, "-f", "compose.yaml", "stop", "notification-service"],
    cwd=ROOT,
    check=True,
)
failed_drain = owner.post("/api/v1/platform/notifications/drain")
assert failed_drain.status_code == 503
```

이 시나리오가 중요한 이유는, "부분 실패"가 어떻게 보이는지를 코드로 보여 주기 때문이다. 댓글은 저장됐지만 알림은 못 갔고, 서비스가 돌아오면 밀린 건 알림이 따라간다.

- 다음: 이 랩은 gateway와 recovery까지 잡고, 서비스별 health/metrics/JSON 로그를 붙이는 분산 운영성은 K-distributed-ops-lab으로 넘긴다.

CLI:

```bash
$ make test
$ python -m pytest tests/test_system.py -q
```

```
1 passed
```

```bash
$ python -m tests.smoke
$ docker compose up --build
```
