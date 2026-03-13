# K-distributed-ops-lab 개발 타임라인

## 2026-03-10
### Session 1

- 목표: J에서 gateway를 만들었는데, "서비스가 준비됐는지"를 외부에서 어떻게 알 수 있나? `/health/ready`라는 말은 들어 봤지만, J의 ready는 그냥 200을 돌려준다. upstream 서비스들이 실제로 살아 있는지는 확인하지 않는다.
- 진행: K의 `health.py`를 열었다. `live`는 여전히 무조건 200이다. 하지만 `ready`가 달랐다.

```python
@router.get("/ready", response_model=HealthResponse)
def ready(
    request: Request,
    client: Annotated[ServiceClient, Depends(get_service_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    try:
        client.request(request, "identity", "GET", "/health/ready")
        client.request(request, "workspace", "GET", "/health/ready")
        client.request(request, "notification", "GET", "/health/ready")
        if settings.redis_url:
            Redis.from_url(settings.redis_url).ping()
    except Exception as exc:
        raise AppError(
            code="DEPENDENCY_NOT_READY",
            message="One or more upstream services are not ready.",
            status_code=503,
        ) from exc
    return HealthResponse(status="ok")
```

- 이슈: internal 서비스 중 하나가 죽어 있으면, gateway의 ready도 503이 된다. 처음엔 "gateway가 ready이면 upstream은 별도로 체크해야 하지 않나?"라고 생각했다. 하지만 이 구조에서 gateway의 ready는 "전체 시스템이 요청을 받을 수 있는가"를 뜻한다. 개별 서비스의 ready는 orchestrator나 load balancer가 직접 각 `/health/ready`를 폴링하면 된다.

CLI:

```bash
$ cd labs/K-distributed-ops-lab/fastapi
$ make install
```

### Session 2

- 목표: G-ops-lab에서 prometheus text 형식으로 `app_requests_total`을 만들었다. K에서는 MSA 구조에서 같은 메트릭을 어떻게 노출하나?
- 진행: `ops.py`를 열었다. 메트릭 엔드포인트는 단일 서비스 시절과 구조가 거의 같다.

```python
@router.get("/metrics", response_class=PlainTextResponse)
def metrics(request: Request) -> str:
    total = request.app.state.metrics.request_count
    return f'app_requests_total{{service="gateway"}} {total}\n'
```

- 이슈: `service="gateway"` 레이블이 붙어 있다. 내부 서비스들도 각자 `service="identity"` 같은 레이블로 메트릭을 내야 scraper가 이름으로 구분할 수 있다. 처음엔 gateway 하나에서 모든 서비스 메트릭을 집계하면 되지 않을까 생각했지만, 그러면 gateway가 내부 서비스의 구현에 결합된다.
- 판단: 각 서비스가 자기 메트릭을 자기 `/ops/metrics`로 내고, scraper가 all-service 엔드포인트를 돌아다니는 게 MSA에서 자연스러운 형태다. gateway는 gateway 자신의 request count만 센다.
- 확인: `main.py`의 middleware에서 `app.state.metrics.increment()`가 모든 요청에 붙어 있으므로, gateway를 통과한 요청 수는 항상 카운트된다.

### Session 3

- 목표: notification-service 장애 후 recovery까지 K의 system test로 확인한다. J에서 이미 같은 시나리오를 봤는데, K에서 추가된 게 있는지 확인한다.
- 진행: `tests/test_system.py`를 J와 비교했다.
- 확인: 핵심 흐름은 동일하다. 하지만 K는 `wait_for("http://127.0.0.1:8133/api/v1/health/ready")`에서 notification-service의 개별 ready를 폴링한다. 이 URL이 notification-service 포트다. 즉, orchestrator가 개별 서비스 ready를 직접 폴링하는 패턴이 system test에 명시적으로 나타난다.

```python
wait_for("http://127.0.0.1:8133/api/v1/health/ready")
recovery_drain = owner.post("/api/v1/platform/notifications/drain")
assert recovery_drain.status_code == 200
assert "Second comment after consumer outage." in websocket.recv(timeout=20)
```

- 판단: K의 핵심은 "각 서비스가 자기 상태를 직접 노출하고, 외부가 그걸 직접 폴링해서 판단한다"는 분산 운영성 원칙이다. gateway의 ready는 편의를 위한 집약이고, 진짜 recovery 여부는 해당 서비스 포트로 확인해야 한다.

CLI:

```bash
$ make test
$ python -m pytest tests/test_system.py -q
```

```
1 passed
```

```bash
$ make smoke
$ docker compose up --build
```
