# C-authorization-lab 개발 타임라인

## 2026-03-09
### Session 1

- 목표: 인증(누구인가)을 끝냈으니 인가(무엇을 할 수 있는가)를 분리해서 만든다. 처음엔 "역할 테이블 하나 추가하면 되는 거 아닌가"라고 생각했다.
- 진행: `problem/README.md`를 읽었다. 워크스페이스, 초대, 역할 변경, 문서 접근 제어가 전부 범위에 들어 있다. 단순 RBAC 테이블이 아니라, 초대 → 수락 → 역할 부여 → 리소스 접근까지의 전체 생명주기를 설명해야 한다.
- 이슈: 이 랩은 인증을 일부러 단순화한다. 로그인 시스템을 붙이지 않고, `X-User-Id` 헤더로 actor를 전달한다. 처음엔 이게 너무 느슨한 거 아닌가 싶었는데, 이 랩의 핵심은 "어떻게 로그인했나"가 아니라 "로그인한 뒤 무엇을 할 수 있는가"이므로 맞는 선택이다.
- 판단: 역할 비교 로직을 먼저 잡고, 그 위에 초대와 문서 접근을 쌓기로 했다.

CLI:

```bash
$ cd labs/C-authorization-lab/fastapi
$ python3 -m venv .venv
$ source .venv/bin/activate
$ make install
```

### Session 2

- 목표: 역할 수준을 비교하는 최소 규칙을 만든다.
- 진행: 처음 시도는 역할별 if-else 체인이었다. viewer면 읽기만, member면 쓰기도, admin이면 초대도... 이러다가 역할이 추가될 때마다 분기가 폭발한다.
- 조치: 역할을 숫자 순서로 매핑해서, "최소 역할" 하나만 비교하는 구조로 바꿨다.

```python
ROLE_ORDER = {"viewer": 1, "member": 2, "admin": 3, "owner": 4}

def _require_role(self, *, actor_id: str, workspace_id: str, minimum: str) -> Membership:
    membership = self.repository.get_membership(workspace_id, actor_id)
    if membership is None or ROLE_ORDER[membership.role] < ROLE_ORDER[minimum]:
        raise AppError(code="FORBIDDEN", message="Forbidden.", status_code=403)
    return membership
```

이 비교 하나로 viewer는 문서를 못 만들고(`minimum="member"`), member는 초대를 못 보내고(`minimum="admin"`), admin은 역할 변경을 못 하는(`minimum="owner"`) 규칙이 전부 설명된다. 처음의 if-else 체인보다 훨씬 깔끔하다.

- 다음: 초대 흐름을 구현한다. 초대가 수락되면 membership이 생겨야 한다.

### Session 3

- 목표: 초대 발행 → 수락/거절 → membership 생성까지 연결한다.
- 진행: `create_invite`에서 admin 이상만 초대를 보낼 수 있게 했다. 초대 토큰은 `secrets.token_urlsafe(18)`로 만든다.
- 이슈: 초대 수락 시점에서 고민이 생겼다. 이미 해당 workspace의 멤버인 사용자가 초대를 수락하면 새 membership을 또 만들어야 하나? 기존 membership이 있으면 스킵하고, 없을 때만 새로 만들기로 했다.

```python
invite.status = "accepted"
membership = self.repository.get_membership(invite.workspace_id, actor.id)
if membership is None:
    membership = Membership(
        user_id=actor.id,
        workspace_id=invite.workspace_id,
        role=invite.role,
    )
```

- 이슈: 초대의 이메일과 수락하는 사용자의 이메일이 다르면? 처음엔 그냥 수락하게 놔뒀는데, 다른 사람이 링크를 가로채서 수락하는 상황이 가능하다. `actor.email != invite.email`이면 403을 던지도록 보호를 넣었다.
- 검증: 거절도 같은 이메일 검사를 거치고, 거절 후 상태가 `declined`로 바뀌는지 확인했다.

CLI:

```bash
$ pytest tests/integration/test_authorization_flows.py -q
```

```
2 passed
```

### Session 4

- 목표: 핵심 시나리오를 하나의 테스트로 관통시킨다. owner가 초대 → viewer가 수락 → 문서 생성 시도 → 403 → owner가 역할 변경 → 문서 생성 성공.
- 진행: 이 흐름이 테스트 하나에 다 들어간다. 처음엔 각 단계를 별도 테스트로 쪼개야 하나 고민했는데, 이 랩의 핵심은 "권한이 바뀌면 바로 다음 요청에 반영되는가"이므로 하나의 연속된 시나리오가 더 설명력이 있다.

```python
forbidden = client.post(
    f"/api/v1/authorization/workspaces/{workspace['id']}/documents",
    json={"title": "Spec"},
    headers={"X-User-Id": viewer["id"]},
)
assert forbidden.status_code == 403

promote = client.patch(
    f"/api/v1/authorization/workspaces/{workspace['id']}/members/{viewer['id']}",
    json={"role": "member"},
    headers={"X-User-Id": owner["id"]},
)
assert promote.status_code == 200
```

이 두 요청 사이에 viewer의 역할이 바뀐다. 403에서 200으로의 전환이 이 랩의 전체 메시지를 압축한다.

- 이슈: outsider(workspace에 속하지 않은 사용자)가 문서를 읽는 것도 막아야 했다. membership이 없으면 `_require_role`에서 바로 403이 나오므로 별도 로직 없이 처리된다.
- 검증: invite accept + document 권한, invite decline + outsider read 차단 두 시나리오 모두 통과.

CLI:

```bash
$ python3 -m compileall app tests
$ make lint
$ make test
```

```
2 passed
```

### Session 5

- 목표: Compose 환경에서 스키마 초기화를 확인한다.
- 이슈: 로컬 학습 환경에서 처음 실행할 때 테이블이 없어서 실패했다. 이 랩은 인증을 뺐기 때문에 migration보다 `lifespan`에서 `create_all`을 부르는 자동 초기화가 더 자연스럽다.
- 조치: 앱 시작 시 스키마 자동 초기화 반영.
- 검증: compile, lint, test, smoke, Compose live/ready probe 모두 통과.
- 다음: 이 랩은 권한 모델까지만 잡고, 데이터 API의 저장 경계(필터, 정렬, 충돌 제어)는 D-data-api-lab으로 넘긴다.

CLI:

```bash
$ make smoke
$ docker compose up --build
```
