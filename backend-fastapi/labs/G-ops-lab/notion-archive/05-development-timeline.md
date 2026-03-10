# 개발 타임라인: G-ops-lab

이 문서는 소스 코드에서 드러나지 않는 개발 과정—환경 설정, 인프라 결정,
Docker 구성, CI 파이프라인, 검증 단계—을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 초기화

```bash
mkdir -p labs/G-ops-lab/fastapi && cd labs/G-ops-lab/fastapi

# pyproject.toml 생성 (name: g-ops-lab-fastapi)
# 핵심 의존성: fastapi, httpx, pydantic-settings, redis, sqlalchemy, uvicorn[standard]
# dev 의존성: pytest, ruff
# ⚠️ psycopg/asyncpg 없음 — SQLite 기본

python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

이 랩은 product domain이 없다. 모델도, 마이그레이션도 없다.
순수하게 운영 표면(health, logging, metrics)만 존재한다.
pyproject.toml에 `psycopg`가 없는 것이 의도적이다.

## Phase 2: core/ — 설정, 로깅, 에러 처리

```python
# app/core/config.py
#   Settings: app_name, environment, api_v1_prefix, database_url, redis_url, allowed_origins
#   @lru_cache get_settings()

# app/core/logging.py
#   JsonFormatter(logging.Formatter) — JSON 로그 출력
#   configure_logging() — root logger 핸들러 교체

# app/core/errors.py
#   AppError exception class
#   register_exception_handlers() — AppError, ValidationError, Exception 전부 포착
```

`configure_logging()`은 `create_app()` 최초 호출 시 실행된다.
이후 모든 `logging.getLogger()` 호출은 JsonFormatter를 사용한다.

Settings의 `database_url` 기본값은 `sqlite+pysqlite:///./g_ops_lab.db`이다.
Compose에서는 `.env`를 통해 PostgreSQL URL로 override한다.

## Phase 3: runtime.py — MetricsRegistry

```python
# app/runtime.py
class MetricsRegistry:
    request_count: int = 0
    def increment(self): self.request_count += 1
```

Prometheus client library 없이 직접 만든 최소 카운터.
`app.state.metrics`에 저장되어 미들웨어와 `/ops/metrics` 라우트에서 공유된다.

```python
# app/main.py 미들웨어
@app.middleware("http")
async def count_requests(request, call_next):
    app.state.metrics.increment()
    return await call_next(request)
```

## Phase 4: Health와 Ops 라우트

```python
# app/api/v1/routes/health.py
#   GET /health/live  → 무조건 {status: "ok"}
#   GET /health/ready → DB SELECT 1 + Redis ping → 성공이면 200, 실패면 503

# app/api/v1/routes/ops.py
#   GET /ops/ready   → Settings 기반 readiness (URL 존재 여부만 검사)
#   GET /ops/metrics → Prometheus text format으로 request_count 노출
```

health와 ops 라우트를 분리한 이유:
- health는 인프라(K8s/Docker) 수준의 probe 대상
- ops는 애플리케이션 관리자가 보는 운영 정보

## Phase 5: DB 세션과 deps

```python
# app/db/session.py
#   configure_engine(): create_engine + sessionmaker 설정
#   get_db(): Session generator (Depends용)

# app/api/deps.py
#   get_metrics_registry(): request.app.state.metrics 반환
```

DB 세션은 health/ready에서만 사용된다 (SELECT 1 검증용).
product 테이블이 없으므로 모델 파일이나 Alembic migration이 존재하지 않는다.

## Phase 6: Docker Compose 구성

```yaml
# compose.yaml — 1개 서비스
services:
  api:       # FastAPI, 포트 8005:8000, uvicorn --reload
             # healthcheck: python urllib으로 /health/live probe
             #   interval: 10s, timeout: 5s, retries: 5, start_period: 15s
```

이 랩의 compose는 API 서비스 하나뿐이다.
PostgreSQL과 Redis가 없다 — 기본 SQLite로 동작한다.
다른 lab(A~F)과 비교하면 가장 가벼운 구성이다.

healthcheck command를 `python -c "import urllib.request; ..."`로 구현해서
curl이 없는 `python:3.12-slim` 이미지에서도 동작한다.

## Phase 7: Dockerfile

```dockerfile
FROM python:3.12-slim
# build-essential, curl 설치
# pyproject.toml + app/ + alembic 복사
# pip install .
# CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`alembic.ini`와 `alembic/`을 COPY하는 이유:
다른 lab과 Dockerfile 구조를 통일하기 위함이며,
실제로 마이그레이션할 테이블은 없다.

## Phase 8: 테스트와 Smoke

```bash
# tests/conftest.py
#   monkeypatch로 DATABASE_URL → SQLite override
#   get_settings.cache_clear() — lru_cache 초기화

# tests/integration/test_ops.py
#   test_live_ready_and_metrics:
#     GET /health/live → 200
#     GET /ops/ready → 200, status=ok
#     GET /ops/metrics → "app_requests_total" 포함

# tests/smoke.py
#   make smoke으로 실행
#   tmpdir에 SQLite DB 생성 → /health/live 호출 → raise_for_status
```

smoke test의 목적: compose 없이 "앱이 뜨는가"를 가장 빠르게 확인한다.
CI에서 compose probe 전에 precheck로 실행한다.

## Phase 9: Makefile과 검증

```bash
make install  # pip install -e ".[dev]"
make lint     # ruff check app tests
make test     # pytest
make smoke    # python -m tests.smoke
make run      # uvicorn --reload
```

CI workflow(`labs-fastapi.yml`)에서는:
1. `make lint`
2. `make test`
3. `make smoke`
4. `docker compose up --build` → healthcheck passing → `compose_probe.sh`

`tools/compose_probe.sh`가 health endpoint를 HTTP로 확인한다.

---

## 타임라인 요약

| 단계 | 핵심 산출물 |
|------|-------------|
| 초기화 | pyproject.toml (product domain 없음) |
| core | config.py, logging.py, errors.py |
| runtime | MetricsRegistry (자체 카운터) |
| 라우트 | /health/live, /health/ready, /ops/ready, /ops/metrics |
| DB 세션 | get_db (health ready 전용) |
| Compose | api 1개 서비스 + healthcheck |
| 테스트 | live, ready, metrics 통합 테스트 + smoke |
| 검증 | lint, test, smoke, Compose probe |
