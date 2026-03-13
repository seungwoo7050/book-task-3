# J-edge-gateway-lab: public API shape는 edge에 남기고, 내부 서비스에는 bearer와 request id만 넘기기

이 글은 `labs/J-edge-gateway-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/J-edge-gateway-lab/fastapi/gateway/app/api/v1/routes/platform.py::_auth_headers`, `labs/J-edge-gateway-lab/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

J 랩의 목적은 서비스 수를 늘리는 데 있지 않다. problem/README.md와 docs/README.md를 보면 핵심 질문은 언제나 public API shape다. 브라우저는 여전히 하나의 /api/v1/auth/*, /api/v1/platform/*만 보되, 내부 서비스에는 cookie와 CSRF를 직접 넘기지 않아야 한다. 이 프로젝트는 기능 추가보다 계약 재설계에 가깝다.

## 1. 서비스 분리 뒤에도 public API shape를 유지해야 한다는 질문 세우기
먼저 gateway를 프록시가 아니라 boundary translator로 본다. README는 request id propagation과 내부 service fan-out을 답안으로 제시하고, docs는 왜 public API를 gateway가 유지해야 하는지, 왜 쿠키와 CSRF를 내부 서비스에 넘기지 않는지를 먼저 묻는다. 그래서 글도 route 목록보다 브라우저 상태와 내부 계약을 분리하는 이유부터 시작하게 된다.

## 2. gateway에 cookie와 bearer 번역 책임을 모으기
코드에서 그 이유를 가장 짧게 보여 주는 건 _auth_headers다. 함수 자체는 짧지만 의미는 크다. gateway는 access token cookie를 읽어 bearer header 하나로 바꾸고, 이후 client.request(...)가 workspace나 notification으로 요청을 넘긴다. 이 작은 번역 단계 덕분에 내부 서비스는 브라우저 상태를 몰라도 된다.

```python
def _auth_headers(request: Request) -> dict[str, str]:
    access_token = request.cookies.get("access_token", "")
    return {"Authorization": f"Bearer {access_token}"}


@router.post("/workspaces", response_model=WorkspaceResponse)
def create_workspace(
    payload: WorkspaceCreateRequest,
    request: Request,
    _: Annotated[dict[str, str], Depends(get_current_claims)],
    client: Annotated[ServiceClient, Depends(get_service_client)],
) -> WorkspaceResponse:
```

핵심은 edge가 cookie를 bearer header로 번역해 내부 서비스 계약을 단순하게 만든다는 데 있다.

## 3. system test로 public path와 internal fan-out을 고정하기
system test는 이 구조를 public API 관점에서 증명한다. owner와 collaborator client 모두 gateway base URL만 사용하고, invite 수락과 project/task/comment 생성, websocket notification 수신까지 모두 public /api/v1/* 경로로 끝낸다. 즉 이 랩이 잘한 일은 서비스 간 호출을 늘린 게 아니라, 외부 사용자가 내부 구조 변화를 몰라도 되게 만든 것이다.

```python
def test_v2_system_flow_and_notification_recovery() -> None:
    with compose_stack() as project_name:
        owner = httpx.Client(base_url="http://127.0.0.1:8013", timeout=10.0)
        collaborator = httpx.Client(base_url="http://127.0.0.1:8013", timeout=10.0)

        register = owner.post(
            "/api/v1/auth/register",
            json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
        )
        assert register.status_code == 200
        verify = owner.post("/api/v1/auth/verify-email", json={"token": _latest_token("owner@example.com")})
        assert verify.status_code == 200
```

테스트는 public `/api/v1`만 호출하면서 invite, comment, websocket 알림까지 닿는지 확인한다.

## 4. 2026-03-10 재검증으로 gateway surface를 닫기
보고서의 2026-03-10 재검증도 그 방향을 따른다. service unit test를 돌린 뒤, 별도로 python -m pytest tests/test_system.py -q와 python -m tests.smoke를 남긴다. gateway는 결국 '서비스별 내부 correctness'와 '외부 public flow'를 둘 다 보여 줘야 설명이 완성된다.

```bash
make test
python -m pytest tests/test_system.py -q
python -m tests.smoke
docker compose up --build
```

2026-03-10에 gateway/identity/workspace/notification unit test, system test, smoke가 모두 통과했다. 이 랩은 브라우저가 public /api/v1/*만 호출한다는 점을 system test가 대신 증명한다.

## 정리
J 랩을 지나면 MSA 설명은 훨씬 제품에 가까워 보이지만, 실제로 새로 배운 것은 public surface를 지키는 법이다. 내부 분해가 외부 계약을 깨뜨리지 않게 만드는 edge 책임이 무엇인지 여기서 선명해진다. 다음 K 랩은 이 분산 구조를 어떻게 관찰할지로 시선을 옮긴다.
