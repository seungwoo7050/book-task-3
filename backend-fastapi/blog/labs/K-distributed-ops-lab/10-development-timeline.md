# K-distributed-ops-lab: 여러 서비스가 함께 살아 있을 때, health와 metrics 질문도 분산시키기

이 글은 `labs/K-distributed-ops-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/routes/ops.py::metrics`, `labs/K-distributed-ops-lab/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

K 랩은 J 랩 뒤에 붙은 마무리처럼 보일 수 있지만, 실제로는 질문이 완전히 다르다. J가 public API shape를 지키는 이야기였다면, K는 여러 서비스가 함께 살아 있을 때 health, metrics, request id, target shape를 어떻게 읽어야 하는지 묻는다. docs/README.md가 gateway health와 내부 service health를 같은 의미로 보면 안 된다고 적는 이유가 바로 그것이다.

## 1. MSA 실행 뒤 남는 운영 질문을 별도 랩으로 떼기
첫 단계에서 운영 질문을 분리한다. README는 서비스별 health/metrics, gateway 포함 Compose health matrix, AWS target shape 문서를 한 답으로 제시한다. 즉 이 프로젝트는 로그를 조금 더 붙이는 작업이 아니라, 분산 구조를 어떤 표면으로 관찰할지를 정리하는 실험이다.

## 2. 서비스별 health/metrics와 gateway health를 다른 질문으로 보기
코드에서는 metrics route가 그 최소 기준을 보여 준다. gateway metrics는 app_requests_total{service="gateway"}라는 한 줄을 반환한다. 아주 작지만, 서비스별 label을 포함해 어떤 주체의 수치인지 분리하려는 의도가 분명하다. compose healthcheck까지 같이 보면 각 서비스가 어떤 준비 상태를 스스로 보고해야 하는지도 보인다.

```python
def metrics(request: Request) -> str:
    total = request.app.state.metrics.request_count
    return f'app_requests_total{{service="gateway"}} {total}\n'
```

여기서는 service label이 붙은 metrics line이 분산 운영성의 최소 관측 surface가 된다.

## 3. system test와 compose health matrix로 운영 surface를 고정하기
system test는 steady-state보다 복구 경로를 강조한다. notification-service를 멈춘 상태에서 두 번째 comment를 남기면 drain이 503이 되고, 서비스를 다시 시작한 뒤 recovery drain을 수행하면 websocket으로 두 번째 알림이 도착한다. 이 흐름 덕분에 운영성 글이 단순 health endpoint 설명에 머물지 않는다.

```python
def test_v2_system_flow_and_notification_recovery() -> None:
    with compose_stack() as project_name:
        owner = httpx.Client(base_url="http://127.0.0.1:8014", timeout=10.0)
        collaborator = httpx.Client(base_url="http://127.0.0.1:8014", timeout=10.0)

        register = owner.post(
            "/api/v1/auth/register",
            json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
        )
        assert register.status_code == 200
        verify = owner.post("/api/v1/auth/verify-email", json={"token": _latest_token("owner@example.com")})
        assert verify.status_code == 200
```

테스트는 분산 runtime이 협업 흐름과 장애 복구를 얼마나 견디는지 마지막 smoke로 보여 준다.

## 4. 2026-03-10 재검증으로 분산 운영성 기준을 닫기
보고서 기준 2026-03-10 재검증은 gateway/identity/workspace/notification unit test, system test, smoke를 모두 남겼다. 운영성 랩일수록 '문서가 있다'보다 '그 문서가 가리키는 runtime이 실제로 다시 올라왔다'는 사실이 더 중요하다. 이 태도가 capstone v2까지 그대로 이어진다.

```bash
make test
make smoke
docker compose up --build
```

2026-03-10에 gateway/identity/workspace/notification unit test, system test, smoke가 통과했다. 이 랩은 '운영성 문서도 학습 산출물'이라는 점을 특히 강하게 보여 준다.

## 정리
K 랩은 분산 운영성도 학습 저장소의 핵심 산출물임을 보여 준다. health와 metrics를 조금 붙였다는 수준이 아니라, 어떤 surface가 service-local이고 어떤 surface가 system-level인지 분리했다는 점이 중요하다. 이것이 capstone v2에서 실제 협업 흐름과 장애 복구를 해석하는 기준이 된다.
