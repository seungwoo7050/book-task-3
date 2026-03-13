# H-service-boundary-lab 개발 타임라인

## 2026-03-10
### Session 1

- 목표: A~G까지 단일 FastAPI로 해 왔는데, 이제 "서비스를 나누는 것"을 처음으로 시도한다. 처음엔 "디렉터리만 나누면 MSA 아닌가?"라고 생각했다.
- 진행: `problem/README.md`를 읽었다. 핵심 질문은 "어디서 경계를 끊어야 하며, 서비스가 서로의 DB를 읽지 않고도 동작할 수 있는가"이다. 단순히 코드를 나누는 게 아니라, 데이터 소유권을 나누는 문제다.
- 이슈: 처음엔 인증과 워크스페이스를 왜 분리해야 하나 의문이었다. 한 서비스에 다 있어도 동작하는데? 하지만 "identity-service의 DB에 있는 사용자 테이블을 workspace-service가 직접 조회한다면?" — 그러면 두 서비스가 같은 DB를 공유해야 하고, 독립 배포가 불가능해진다.
- 판단: `identity-service`는 토큰만 발급하고, `workspace-service`는 그 토큰의 claims만 읽어서 workspace를 만드는 구조로 가기로 했다.

CLI:

```bash
$ cd labs/H-service-boundary-lab/fastapi
$ make install
```

### Session 2

- 목표: 두 서비스 사이의 경계를 system test로 고정한다.
- 진행: `test_system.py`를 작성했다. identity-service에서 register → verify → login으로 access_token을 받고, 그 토큰으로 workspace-service에 workspace를 만드는 흐름이다.
- 이슈: 처음엔 workspace-service에서 사용자 정보가 필요해서 identity-service의 DB를 읽으려 했다. 이렇게 하면 경계가 무너진다.
- 조치: workspace-service는 bearer token에 들어 있는 claims(sub, handle)만 사용하고, identity DB를 직접 읽지 않는다.

```python
access_token = login.json()["access_token"]
create_workspace = workspace.post(
    "/internal/workspaces",
    json={"name": "Alpha"},
    headers={"Authorization": f"Bearer {access_token}"},
)
```

이 테스트 조각은 단순해 보이지만, "workspace-service가 identity-service의 DB를 조회하지 않는다"는 경계를 코드 수준에서 증명한다. access_token 안의 claims만으로 다음 단계가 진행된다.

- 검증: system test에서 register → verify → login → workspace creation까지 통과.

CLI:

```bash
$ python -m pytest tests/test_system.py -q
```

```
1 passed
```

### Session 3

- 목표: gateway 계층의 시작점인 request id 전파를 만든다.
- 진행: 이 랩에는 아직 완전한 gateway가 없지만, request id middleware의 초기 형태를 gateway 쪽에 넣었다. 이후 J, K에서 계속 재사용될 패턴이다.

```python
request_id = request.headers.get("X-Request-ID", str(uuid4()))
request.state.request_id = request_id
token = set_request_id(request_id)
app.state.metrics.increment()
response = await call_next(request)
response.headers["X-Request-ID"] = request_id
```

처음엔 request id가 왜 필요한지 확실하지 않았다. 서비스가 하나면 로그를 보면 되니까. 하지만 서비스가 둘 이상이면, 하나의 요청이 어디서 시작해서 어디로 흘러갔는지 추적하려면 공통 ID가 필요하다. 이 middleware가 그 시작점이다.

- 검증: lint, test, smoke 통과. Compose에서 두 서비스가 실제로 분리된 포트(8011, 8111)에서 뜨는 것을 확인했다.
- 다음: 이 랩은 서비스 경계 분리까지만 잡고, outbox와 이벤트 통합은 I-event-integration-lab으로 넘긴다.

CLI:

```bash
$ make lint
$ make test
$ make smoke
$ docker compose up --build
```
