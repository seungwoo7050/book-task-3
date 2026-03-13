# C-authorization-lab: 로그인에서 한 걸음 물러서서, 누가 무엇을 할 수 있는지만 고립시키기

이 글은 `labs/C-authorization-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py::create_invite`, `labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py::test_invite_accept_promote_and_document_permissions`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

C 랩은 앞선 인증 트랙 뒤에 오지만, 실제로는 한 걸음 뒤로 물러선 프로젝트다. problem/README.md는 '누가 무엇을 할 수 있는가'를 명확히 해야 한다고만 말하고, README.md는 실제 로그인 시스템을 제외 범위로 밀어낸다. 이 결정 덕분에 글도 '어떻게 로그인했는가'가 아니라 '어떤 actor가 언제 403을 받아야 하는가'를 중심으로 재구성할 수 있다.

## 1. 로그인 대신 actor와 역할표부터 세우기
출발점부터 actor 모델을 단순화했다. fastapi/README.md의 실행 surface는 단순하지만, docs/README.md가 먼저 묻는 질문은 역할과 소유권의 차이, 초대 흐름에서 누가 상태를 바꿀 수 있는가, 인가 규칙을 테스트하기 좋은 경계가 어디인가 같은 것들이다. 인증을 빼낸 자리에 역할표와 invitation lifecycle이 들어앉은 셈이다.

## 2. 초대 lifecycle을 인가 규칙의 중심으로 잡기
그래서 중심 route도 authorization.py 하나로 모인다. create_invite, accept_invite, decline_invite, change_role, create_document, get_document가 한 surface에 있는 구성이 중요하다. 이 파일은 인가를 '모든 endpoint에 if를 붙이는 일'이 아니라 'workspace membership과 invitation 상태를 전이시키는 일'로 재정의한다.

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

이 대목에서 드러나는 건 인가 규칙이 actor, workspace, role payload를 함께 받아 판단한다는 사실이다.

## 3. 권한 상승과 접근 거부를 테스트로 고정하기
테스트는 그 전이를 구체적으로 보여 준다. viewer가 초대를 수락한 직후에는 문서 생성이 403이고, owner가 role을 member로 바꾼 다음에야 200이 된다. 다른 테스트에서는 초대를 decline한 invitee와 outsider 읽기 실패까지 확인한다. 이 흐름이 있으니 글에서도 '권한 테이블을 만들었다'가 아니라 '권한 상승 전후의 API 의미가 어떻게 달라지는지'를 자연스럽게 따라갈 수 있다.

```python
def test_invite_accept_promote_and_document_permissions(client) -> None:
    owner = client.post(
        "/api/v1/authorization/users",
        json={"email": "owner@example.com", "name": "Owner"},
    ).json()
    viewer = client.post(
        "/api/v1/authorization/users",
        json={"email": "viewer@example.com", "name": "Viewer"},
    ).json()

    workspace = client.post(
        "/api/v1/authorization/workspaces",
```

테스트는 viewer가 거절당했다가 promote 뒤 허용되는 전환을 그대로 남긴다.

## 4. 2026-03-09 재검증으로 규칙 surface를 다시 확인하기
재검증 단계에서는 이 규칙이 독립 워크스페이스로 돌아간다는 사실이 닫힌다. 보고서에 적힌 2026-03-09 재실행은 compile, lint, test, smoke, Compose probe를 모두 포함하고, 로컬 실행을 위해 스키마 자동 초기화를 남겼다. 인가 규칙이 추상 정책 문서가 아니라 실제 FastAPI 앱으로 살아 있다는 증거다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh labs/C-authorization-lab/fastapi 8001
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다. 이 랩은 로그인 시스템을 의도적으로 비워 두므로, 검증도 actor header 기반 규칙 surface에 집중한다.

## 정리
C 랩이 하는 일은 로그인 시스템을 대체하는 것이 아니라, 로그인과 별개로 인가 규칙을 설명 가능한 단위로 떼어내는 것이다. 이 덕분에 다음 D 랩에서는 '누가 할 수 있는가'를 잠시 내려놓고, 데이터 API 자체가 어떤 일관성을 가져야 하는지에만 집중할 수 있다.
