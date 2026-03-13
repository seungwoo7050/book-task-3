# G-ops-lab: 기능보다 먼저, 앱이 살아 있고 준비됐다는 질문을 분리하기

이 글은 `labs/G-ops-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py::metrics`, `labs/G-ops-lab/fastapi/tests/integration/test_ops.py::test_live_ready_and_metrics`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

G 랩은 기능을 하나 더 만드는 프로젝트가 아니다. 오히려 기능을 거의 비워 둔 채, 앱이 살아 있는지, 준비됐는지, 최소 metrics가 어떤 질문에 답하는지, CI와 target shape 문서를 어떻게 구분할지에 집중한다. problem/README.md와 docs/README.md를 같이 읽으면 이 랩이 왜 별도 주제가 되었는지 바로 보인다.

## 1. 운영성을 기능 뒤에 숨기지 않고 별도 랩으로 떼기
출발점에서부터 운영성은 부록이 아니다. README는 live/ready health, request-count metrics, JSON 로그, GitHub Actions, AWS target shape 문서를 한 묶음으로 제시한다. 즉 이 프로젝트는 '운영 도구도 좀 붙였다'가 아니라, 운영 질문만 따로 떼어 연습하는 워크스페이스다.

## 2. live/ready와 metrics를 별도 route로 굳히기
코드에서 가장 분명한 조각은 metrics route다. 이 함수는 state에 쌓인 request count를 Prometheus text 형식으로 바로 노출한다. 아주 작지만, 어떤 수치를 왜 내보내는지 설명 가능하게 만든다는 점에서 이 랩의 목적과 정확히 맞아떨어진다. 같은 이유로 ready와 live를 다른 route로 나눠 둔 것도 중요하다.

```python
def metrics(
    registry: Annotated[MetricsRegistry, Depends(get_metrics_registry)],
) -> Response:
    body = (
        "# HELP app_requests_total Total HTTP requests handled\n"
        "# TYPE app_requests_total counter\n"
        f"app_requests_total {registry.request_count}\n"
    )
    return Response(content=body, media_type="text/plain; version=0.0.4")
```

여기서는 최소 metrics가 어떤 운영 질문에 답하는지 바로 읽힌다.

## 3. 테스트와 workflow로 운영 surface를 닫기
테스트와 workflow가 이 surface를 굳힌다. tests/integration/test_ops.py는 live 200, ready 200, metrics text 안의 app_requests_total을 차례로 확인한다. 거기에 .github/workflows/labs-fastapi.yml이 이 workspace를 matrix로 따로 돌리고, tools/compose_probe.sh가 live/ready를 다시 probe한다. 운영성은 결국 자동 검증의 모양으로 남아야 한다는 뜻이다.

```python
def test_live_ready_and_metrics(client) -> None:
    live = client.get("/api/v1/health/live")
    assert live.status_code == 200

    ready = client.get("/api/v1/ops/ready")
    assert ready.status_code == 200
    assert ready.json()["status"] == "ok"

    metrics = client.get("/api/v1/ops/metrics")
    assert metrics.status_code == 200
    assert "app_requests_total" in metrics.text
```

테스트는 live, ready, metrics 세 surface가 함께 회귀선이 된다는 점을 남긴다.

## 4. 2026-03-09 재검증으로 문서와 실행을 맞추기
재검증 보고서는 한 가지 태도를 더 남긴다. 2026-03-09에 compile, lint, test, smoke, Compose probe가 통과한 사실은 사실대로 적고, AWS 문서는 target shape로만 남긴다. 배포를 자동화하지 않았는데도 그 경계를 숨기지 않는 점이 이 프로젝트의 품질을 더 안정적으로 만든다.

```bash
python3 -m compileall app tests
make lint
make test
make smoke
./tools/compose_probe.sh labs/G-ops-lab/fastapi 8005
```

2026-03-09에 compile, lint, test, smoke, Compose live/ready probe가 모두 통과했다. 이 랩은 target shape 문서를 실제 배포 사실처럼 쓰지 않는 것이 중요한 검증 태도다.

## 정리
G 랩은 운영성도 코드와 문서, CLI, 검증이 함께 있어야 설명 가능하다는 사실을 보여 준다. 이 기준이 있었기 때문에 단일 앱 capstone과 뒤이은 MSA 트랙에서도 '무엇이 실제 검증된 사실인가'를 더 엄격하게 구분할 수 있게 됐다.
