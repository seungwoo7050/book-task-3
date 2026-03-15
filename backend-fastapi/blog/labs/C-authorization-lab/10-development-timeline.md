# C-authorization-lab development timeline

이 글은 C 랩을 "간단한 RBAC 예제"처럼 다루지 않는다. 현재 남아 있는 source of truth를 따라가 보면, 이 프로젝트의 핵심은 인증 자체를 단순화한 뒤에도 인가 규칙이 흐트러지지 않게 만드는 데 있다. `X-User-Id`라는 최소 actor 입력만 남겨 놓고, workspace membership, invitation status, owner/member/viewer 임계값, 문서 접근 제어를 어디서 서비스 규칙으로 고정하는지가 실제 중심이다.

## Phase 1. 인증을 비우고 actor 입력만 남긴다

가장 먼저 확인할 건 [`get_actor_id()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/deps.py) 이다. 이 랩은 세션, JWT, cookie를 아예 다루지 않고 `X-User-Id` 헤더 하나를 actor 입력으로 받는다. README가 인증을 제외 범위로 밀어낸 이유가 여기서 바로 구현으로 드러난다.

이 선택은 꽤 의도적이다. 인가를 설명할 때 "누가 들어왔는가"와 "들어온 뒤 무엇을 할 수 있는가"를 섞지 않기 위해서다. 그래서 C 랩은 auth surface를 거의 비운 대신, authorization route 하나에 user, workspace, invite, membership, document 규칙을 몰아 둔다.

## Phase 2. invitation lifecycle이 authorization의 중심 surface가 된다

[`authorization.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py) 를 보면 중심 endpoint는 `create_invite`, `accept_invite`, `decline_invite`, `change_role`, `create_document`, `get_document`다. 이 배열이 중요한 이유는 인가를 "리소스 읽기/쓰기 전에 검사 하나 넣기"가 아니라, membership과 invite 상태를 전이시키는 문제로 다시 정의하기 때문이다.

```python
def create_invite(
    workspace_id: str,
    payload: CreateInviteRequest,
    actor_id: Annotated[str, Depends(get_actor_id)],
    service: Annotated[AuthorizationService, Depends(get_authorization_service)],
) -> InviteResponse:
    invite = service.create_invite(
        actor_id=actor_id,
        workspace_id=workspace_id,
        email=payload.email,
        role=payload.role,
    )
```

여기서 인가 판단의 최소 입력이 보인다. actor, workspace, email, role이다. 로그인 방식은 필요 없고, "누가 누구를 어떤 역할로 초대하려 하는가"만 있으면 된다.

## Phase 3. ROLE_ORDER가 권한 임계값을 서비스 계층으로 고정한다

실제 규칙은 [`AuthorizationService`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/domain/services/authorization.py) 의 `ROLE_ORDER`와 `_require_role()` 안에 모여 있다. `viewer < member < admin < owner` 순서를 기준으로 invite 생성은 최소 `admin`, 문서 생성은 최소 `member`, 문서 읽기는 최소 `viewer`, role change는 사실상 `owner`만 허용된다.

```python
ROLE_ORDER = {"viewer": 1, "member": 2, "admin": 3, "owner": 4}

def _require_role(self, *, actor_id: str, workspace_id: str, minimum: str) -> Membership:
    membership = self.repository.get_membership(workspace_id, actor_id)
    if membership is None or ROLE_ORDER[membership.role] < ROLE_ORDER[minimum]:
        raise AppError(code="FORBIDDEN", message="Forbidden.", status_code=403)
    return membership
```

이 랩이 깔끔한 건 권한 판단이 route에 흩어지지 않고 서비스 계층에서 하나의 임계값 규칙으로 읽힌다는 점이다. owner-only role change를 굳이 한 번 더 검사하는 것도 이 랩이 소유권을 역할표와 분리해서 강조하려는 흔적이다.

## Phase 4. invitation은 수락 여부보다 "누가 그 상태를 바꿀 수 있는가"가 더 중요하다

`accept_invite()`와 `decline_invite()`를 보면 둘 다 invite token만으로 끝나지 않는다. acting user가 실제로 그 email의 주인인지 다시 확인하고, 아니면 `INVITE_EMAIL_MISMATCH`로 막는다. 즉 이 랩의 invitation rule은 "token을 아는가"보다 "그 token이 누구를 대상으로 발급됐는가"를 더 중요하게 본다.

이 지점에서 invitation lifecycle이 단순 CRUD가 아니라 상태 전이로 보이기 시작한다. `pending -> accepted` 또는 `pending -> declined`는 아무나 바꿀 수 있는 값이 아니라, actor identity와 연결된 상태다.

## Phase 5. 테스트가 승격 전후의 403/200 경계를 고정한다

이 랩의 가장 좋은 문서는 통합 테스트다. [`test_invite_accept_promote_and_document_permissions()`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py) 는 viewer가 초대를 받아도 바로 문서를 만들 수는 없고, owner가 role을 `member`로 올려 준 다음에야 200이 된다는 걸 한 흐름으로 보여 준다.

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

다른 테스트는 초대 거절과 outsider read 금지를 고정한다. 이 덕분에 C 랩의 핵심은 허용 규칙 표를 예쁘게 만드는 일이 아니라, "정확히 언제 403이어야 하는가"를 회귀선으로 남기는 일이라는 점이 더 또렷해진다.

## Phase 6. 오늘 다시 돌린 검증은 path 문제와 schema dependency 문제를 같이 드러냈다

2026-03-14 현재 셸에서 다시 실행한 결과는 공식 문서보다 거칠다.

```bash
make lint
make test
make smoke
PYTHONPATH=. pytest
PYTHONPATH=. python -m tests.smoke
```

오늘 확인한 결과는 이렇다.

- `make lint`: [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/v1/routes/health.py) 의 주석 한 줄이 `E501`로 실패한다.
- `make test`: `ModuleNotFoundError: No module named 'app'`.
- `make smoke`: Homebrew `python3` 기준 `ModuleNotFoundError: No module named 'fastapi'`.
- `PYTHONPATH=. pytest`: [`schemas/authorization.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/schemas/authorization.py) 의 `EmailStr`가 기대하는 `email-validator` 부재로 실패한다.
- `PYTHONPATH=. python -m tests.smoke`: 같은 `email-validator` import 단계에서 실패한다.

이건 꽤 중요한 정보다. 이 랩의 규칙 설계는 선명하지만, 지금 셸에서 공식 재검증 surface는 path 설정과 schema dependency에서 먼저 깨진다. 문서가 이 사실을 빼면 구현 완성도보다 실행 재현성이 더 좋아 보이게 된다.

## 정리

C-authorization-lab이 실제로 한 일은 인증을 대체하는 것이 아니다. 오히려 반대다. 인증을 거의 비워 둔 상태에서도 인가 규칙이 standalone으로 설명될 수 있는지를 시험한다. actor header, invite email match, ROLE_ORDER, owner-only role change, viewer/member document threshold가 서로 연결되면서, "누가 무엇을 할 수 있는가"가 하나의 서비스 규칙 집합으로 읽히게 된다. 다음 D 랩이 데이터 API 일관성에 집중할 수 있는 것도, 여기서 권한 규칙이 한 번 분리되어 있기 때문이다.
