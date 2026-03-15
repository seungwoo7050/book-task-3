# G-ops-lab development timeline

이 글은 G 랩을 "마지막에 health와 metrics를 붙인 예제"로 요약하지 않는다. 현재 남아 있는 source of truth를 따라가면, 이 프로젝트의 핵심은 운영 질문을 기능 뒤에 숨기지 않고 별도 표면으로 세우는 데 있다. 실제로 중요한 건 live, dependency-ready, config-ready, request counter, JSON logging, 그리고 실제 배포 사실이 아닌 target shape 문서를 서로 섞지 않는 태도다.

## Phase 1. 문제 정의가 기능보다 운영 질문을 먼저 올린다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/problem/README.md), [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/docs/README.md), [`docs/aws-deployment.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/docs/aws-deployment.md) 를 같이 보면, 이 랩이 먼저 묻는 건 "무슨 API를 제공하는가"가 아니라 "이 앱이 살아 있고 준비됐다는 말을 어떤 근거로 할 것인가"에 가깝다. live/ready, metrics, Compose/CI, AWS target shape가 한 묶음으로 나오는 이유도 여기에 있다.

특히 AWS 문서가 "실제 배포가 검증되었다는 뜻이 아니다"라고 못 박는 점이 중요하다. G 랩은 운영성 문서에서 가장 위험한 과장을 먼저 차단한다. 구현된 것과 상정한 것을 섞지 않는 태도가 이 프로젝트의 중심이다.

## Phase 2. live, dependency-ready, config-ready는 일부러 다른 route로 남아 있다

이 랩의 가장 흥미로운 점은 ready가 하나가 아니라 두 종류로 읽힌다는 것이다. [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/health.py) 의 `GET /health/ready`는 DB와 optional Redis를 실제로 probe한다. 반면 [`ops.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py) 의 `GET /ops/ready`는 `database configured`, `redis configured/skipped` 같은 구성 요약을 반환한다.

```python
@router.get("/ready", response_model=dict)
def ready() -> dict[str, object]:
    settings = get_settings()
    return {
        "status": "ok",
        "checks": {
            "database": "configured" if settings.database_url else "missing",
            "redis": "configured" if settings.redis_url else "skipped",
        },
    }
```

이 구조 덕분에 G 랩은 "준비됐다"는 말을 하나의 의미로 뭉개지 않는다. process가 살아 있는가, dependency가 응답하는가, 설정이 들어갔는가는 서로 다른 질문이 된다.

## Phase 3. metrics는 의도적으로 작은 인메모리 counter에서 멈춘다

[`runtime.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/runtime.py) 와 [`main.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/main.py) 를 보면 metrics는 아주 작은 모델이다. `MetricsRegistry`는 `request_count` 하나만 들고 있고, 앱 middleware는 모든 HTTP 요청마다 그 값을 증가시킨다. [`ops.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/ops.py) 는 그 값을 Prometheus text 형식으로 노출한다.

```python
@app.middleware("http")
async def count_requests(request: Request, call_next):
    app.state.metrics.increment()
    return await call_next(request)
```

여기서 중요한 건 무엇을 하지 않는지도 같이 보인다는 점이다. 이 metrics는 프로세스 재시작 시 초기화되고, 외부 exporter나 TSDB와 붙지 않는다. 대신 "최소 surface가 무엇인가"를 설명하기에는 충분하다. `metrics` 요청 자체도 카운트에 포함된다고 읽히는 이유 역시 이 middleware 위치 덕분이다. 이것은 코드에서의 추론이다.

## Phase 4. JSON logging과 target-shape 문서는 운영성의 다른 층위를 보여 준다

[`logging.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/core/logging.py) 는 매우 단순한 JSON formatter를 둔다. timestamp, level, logger, message만 남기고, 구조화 로그가 왜 운영 표면인지 보여 준다. 이것도 full observability stack이 아니라 "운영 질문을 위해 최소한 어떤 로그 모양이 필요한가"에 가깝다.

반대로 AWS 문서는 코드가 아니라 문서 층위다. ECS Fargate, ECR, RDS, ElastiCache, Secrets Manager, CloudWatch Logs를 나열하지만, 어디까지나 target shape 요약이다. 이 구분 덕분에 G 랩은 배포가 끝난 것처럼 행동하지 않고, "클라우드로 옮긴다면 어떤 조합을 상정했는가"만 남긴다.

## Phase 5. 테스트는 ops surface가 실제 회귀선인지 확인한다

[`test_ops.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/tests/integration/test_ops.py) 는 작지만 이 랩의 의도를 잘 보여 준다. `live`, `ops/ready`, `ops/metrics`를 차례로 호출하고 `app_requests_total`이 metrics text에 들어 있는지 확인한다.

```python
live = client.get("/api/v1/health/live")
assert live.status_code == 200

ready = client.get("/api/v1/ops/ready")
assert ready.status_code == 200
assert ready.json()["status"] == "ok"

metrics = client.get("/api/v1/ops/metrics")
assert metrics.status_code == 200
assert "app_requests_total" in metrics.text
```

이 테스트는 dependency-ready probe까지 모두 확인하지는 않지만, 운영 표면이 문서 속 설명이 아니라 실제 API contract라는 점은 분명히 고정한다. smoke는 `/health/live`만 확인해 최소 부팅 가능성을 빠르게 닫는다.

## Phase 6. 오늘 다시 돌린 검증은 ops surface 자체와 기본 진입점 문제를 분리해서 보여 준다

2026-03-14 현재 셸에서 다시 실행한 명령은 아래와 같다.

```bash
make lint
make test
make smoke
PYTHONPATH=. pytest
PYTHONPATH=. python -m tests.smoke
```

오늘 확인한 결과는 이렇게 갈렸다.

- `make lint`: [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/G-ops-lab/fastapi/app/api/v1/routes/health.py) 의 예외 주석 한 줄이 `E501`로 실패한다.
- `make test`: `ModuleNotFoundError: No module named 'app'`.
- `make smoke`: Homebrew `python3` 기준 `ModuleNotFoundError: No module named 'fastapi'`.
- `PYTHONPATH=. pytest`: 통합 테스트 1개 통과. 다만 `pytest_asyncio` deprecation warning이 남는다.
- `PYTHONPATH=. python -m tests.smoke`: `/api/v1/health/live` 200으로 통과.

즉 G 랩은 현재 셸에서도 ops surface 자체는 살아 있다. 하지만 기본 `make` 진입점은 여전히 import path와 interpreter 선택 때문에 바로 닫히지 않는다. 이 차이를 남겨야 "운영 표면은 구현돼 있다"와 "공식 검증 루프는 아직 정리 중이다"를 동시에 전달할 수 있다.

## 정리

G-ops-lab이 실제로 남기는 건 health endpoint 몇 개가 아니다. alive, dependencies ready, config summary, request counter, JSON logging, target-shape 문서를 서로 다른 층위로 나누는 태도다. 현재 구현은 metrics와 로그를 아주 작은 인메모리 모델로 보여 주고, AWS는 문서 수준 shape로만 남겨 둔다. 이 기준이 있었기 때문에 이후 capstone에서도 "무엇이 실제로 검증된 운영 surface인가"를 더 엄격하게 읽을 수 있게 된다.
