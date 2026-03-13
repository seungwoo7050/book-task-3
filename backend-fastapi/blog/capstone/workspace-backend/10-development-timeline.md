# workspace-backend: 분리해서 배운 경계들을 하나의 협업형 백엔드 안에서 다시 조합하기

이 글은 `capstone/workspace-backend/README.md`, `problem/README.md`, `docs/README.md`, `capstone/workspace-backend/fastapi/app/api/v1/routes/platform.py::create_comment`, `capstone/workspace-backend/fastapi/tests/integration/test_capstone.py::test_local_auth_workspace_flow_and_google_member_notification`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

workspace-backend capstone은 A~G 랩을 한 폴더에 모아 둔 결과물이 아니다. problem/README.md와 docs/README.md를 보면, 질문은 '기능을 얼마나 많이 합쳤는가'보다 '인증, 인가, 데이터 API, 알림, 실시간 전달이 어디서 만나고 어디서 분리되는가'에 가깝다. 그래서 글도 기능 목록보다 협업 흐름이 한 사용자에서 다른 사용자로 어떻게 번지는지에 초점을 둔다.

## 1. 랩의 답을 제품 도메인으로 다시 묶기
처음에는 랩에서 익힌 경계를 제품 도메인으로 다시 정리해야 했다. README가 로컬 로그인과 Google 로그인, workspace membership, project/task/comment API, queued notification, realtime delivery를 한 답으로 제시하는 이유가 바로 그것이다. 랩 코드를 공용 패키지로 뽑지 않고 다시 구현했다는 문장도, 조합 과정이 단순 재사용이 아니었음을 말해 준다.

## 2. platform route에 협업 흐름을 한데 모으기
코드에서 그 재조합이 가장 잘 보이는 곳은 platform.py다. 여기에는 workspace 생성부터 invite, project, task, comment, notification drain, presence, websocket route까지 모두 들어 있다. 특히 create_comment는 겉보기엔 작은 route지만, 실제로는 데이터 API와 비동기 알림, 실시간 전달이 만나는 중심점이다.

```python
def create_comment(
    task_id: str,
    payload: CommentCreateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[PlatformService, Depends(get_platform_service)],
) -> CommentResponse:
    comment = service.create_comment(actor=current_user, task_id=task_id, body=payload.body)
    return CommentResponse(id=comment.id, task_id=comment.task_id, author_user_id=comment.author_user_id, body=comment.body)


@router.post("/notifications/drain", response_model=dict)
async def drain_notifications(
```

핵심은 댓글 생성이 알림과 실시간 전달로 이어지는 통합 지점이라는 데 있다.

## 3. 통합 테스트로 조합이 실제로 이어지는지 확인하기
통합 테스트는 이 구조를 실제 사용자 시나리오로 고정한다. owner는 로컬 계정으로 가입/검증/로그인하고, collaborator는 Google 로그인으로 들어온다. owner가 workspace를 만들고 invite를 보내면 collaborator가 수락하고, 이후 댓글이 생성되면 collaborator의 websocket으로 알림이 도착한다. 이 흐름이 있기 때문에 capstone 글도 기능 요약이 아니라 '행위가 어떻게 연결되는가'를 따라갈 수 있다.

```python
def test_local_auth_workspace_flow_and_google_member_notification(app_client: TestClient) -> None:
    owner = app_client
    register = owner.post(
        "/api/v1/auth/register",
        json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
    )
    assert register.status_code == 200
    verify = owner.post("/api/v1/auth/verify-email", json={"token": _latest_token(owner)})
    assert verify.status_code == 200
    login = owner.post(
        "/api/v1/auth/login",
        json={"email": "owner@example.com", "password": "super-secret-1"},
```

테스트는 소유자 로컬 로그인, 협업자 Google 로그인, 초대, websocket 알림을 끝까지 통과시킨다.

## 4. 2026-03-09 재검증으로 단일 백엔드 기준선을 닫기
재검증 보고서는 이 단일 백엔드가 단순 문서 예제가 아니라 실제 기준선이라는 사실을 닫는다. 2026-03-09에 compile, lint, test, smoke, Compose probe가 모두 통과했고, 로컬 실행 편의를 위한 스키마 자동 초기화가 따로 기록돼 있다. 이 기록 덕분에 나중에 v2 MSA를 볼 때도 무엇이 기준선인지 흐려지지 않는다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh capstone/workspace-backend/fastapi 8010
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 통과했고, 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화를 두었다. 이 프로젝트는 이후 v2 MSA와 비교되는 단일 백엔드 기준선이기 때문에, verification 기록이 특히 중요하다.

## 정리
이 capstone이 남기는 가장 큰 가치는 완성된 제품 흉내가 아니라 비교 기준선이다. 여기서 한 프로세스 안에 묶였던 것들이 다음 v2에서 어떤 비용을 치르고 분리되는지, 바로 그 차이를 설명하기 위한 출발점이 된다.
