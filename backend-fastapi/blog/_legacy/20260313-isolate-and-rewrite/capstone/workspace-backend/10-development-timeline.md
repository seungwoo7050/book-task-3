# workspace-backend 개발 타임라인

## 2026-03-09
### Session 1

- 목표: A부터 G까지 7개 랩을 각각 따로 다뤘는데, 실제로 한 서비스 안에 같이 들어가면 어떤 문제가 생길까? "단순히 코드를 합치면 되는 것 아닌가?"라고 생각했다.
- 진행: `problem/README.md`를 읽었다. 문제 중 하나가 눈에 들어왔다. comment 작성자는 알림 대상이 아니다. local login 사용자와 Google login 사용자가 같은 workspace에 들어올 수 있다. 그런데 두 사람이 websocket notification을 받는 route는 하나다.
- 이슈: `access_token`이 로그인 방식에 따라 다른 형태로 발급되면 안 된다. `collaborator = TestClient(owner.app)`으로 같은 앱 인스턴스를 공유하는데, Google login 경로로 받은 access_token이 websocket 인증에 그대로 쓰인다.

```python
google_login = collaborator.post(
    "/api/v1/auth/google/login",
    json={"subject": "google-123", "email": "collab@example.com", "display_name": "Collab"},
)
access_token = collaborator.cookies["access_token"]
...
with collaborator.websocket_connect(f"/api/v1/platform/ws/notifications?access_token={access_token}") as websocket:
```

- 판단: 인증 방식이 달라도 access_token payload 구조(sub, exp 등)가 동일해야 websocket route가 투명하게 처리할 수 있다. B 랩에서 만든 `sync_google_user`가 여기서 중요해진다.

CLI:

```bash
$ cd capstone/workspace-backend/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: comment 저장 후 알림 큐 적재를 어디에 두어야 하나? notification 전송은 비동기인데, comment 저장은 동기 DB 트랜잭션이다.
- 진행: `domain/services/platform.py`의 `create_comment`를 봤다.

```python
def create_comment(self, *, actor: User, task_id: str, body: str) -> Comment:
    ...
    comment = Comment(task_id=task.id, author_user_id=actor.id, body=body)
    self.repository.save(comment)
    for member in self.repository.list_workspace_members(project.workspace_id):
        if member.user_id != actor.id:
            self.repository.save(
                Notification(
                    recipient_user_id=member.user_id,
                    message=f"New comment on task {task.title}: {body}",
                    status="queued",
                )
            )
    self.session.commit()
```

- 이슈: comment와 Notification 행이 같은 `session.commit()`에 묶인다. "commit 전에 알림을 보내면 comment가 저장되기 전에 websocket이 먼저 울리지 않나?" → 처음엔 그렇게 생각했다. 하지만 코드를 보면 저장 → commit → drain 세 단계가 분리돼 있다.
- 진행: `drain_notifications`는 별도 API 호출이다. commit이 끝난 뒤에야 `queued` 상태인 Notification 행을 읽어서 websocket으로 보낸다.

```python
async def drain_notifications(self) -> int:
    notifications = self.repository.list_queued_notifications()
    for notification in notifications:
        await self.manager.send_notification(
            user_id=notification.recipient_user_id,
            payload={"message": notification.message},
        )
        notification.status = "sent"
    self.session.commit()
    return len(notifications)
```

- 판단: commit 전 알림 적재 → commit 확인 → drain 호출로 알림 전송. E 랩에서 배운 outbox 패턴의 단일 서비스 버전이다. MSA가 아니어도 같은 원리가 적용된다.

### Session 3

- 목표: schema 자동 초기화. 로컬에서 alembic 마이그레이션을 수동으로 실행하지 않아도 테스트가 돌아야 한다.
- 진행: `main.py`의 lifespan을 봤다.

```python
@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_schema()
    yield
```

- `initialize_schema()`가 뭔가 봤더니 SQLAlchemy의 `metadata.create_all(bind=engine)`을 부르는 wrapper다. 테스트 환경에서는 SQLite in-memory로 교체되기 때문에 alembic 없이 항상 최신 스키마로 시작한다.
- 판단: G 랩에서 배웠던 "테스트는 스키마 자동 초기화, 프로덕션은 alembic" 구분이 여기서도 이어진다.

### Session 4

- 목표: 전체 통합 테스트 실행.
- 진행: `tests/integration/test_capstone.py`가 owner local signup→verify→login, collaborator Google login, workspace invite, project→task→comment, drain, websocket 수신까지 한 파일로 돌아간다.

```bash
$ pytest tests/integration/test_capstone.py -q
```

```
1 passed
```

- 이슈: 왜 `collaborator = TestClient(owner.app)`를 따로 만들어야 하는지 처음엔 헷갈렸다. 한 client로 owner와 collaborator를 같이 처리하면 cookie jar가 섞여서 "누가 로그인한 상태인지"가 흐려진다.
- 정리: 테스트가 owner와 collaborator를 별도 client로 분리한 이유는 쿠키 상태를 명확히 분리하기 위해서다. 그 덕분에 Google login으로 받은 collaborator의 `access_token`을 websocket 인증에 그대로 연결할 수 있다.
- 다음: 여기까지가 단일 서비스 기준선. v2에서는 이 흐름을 gateway + 3개 서비스로 분리하고, gateway가 cookie를 edge에서만 다룬다.

CLI:

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
$ make smoke
$ docker compose up --build
```
