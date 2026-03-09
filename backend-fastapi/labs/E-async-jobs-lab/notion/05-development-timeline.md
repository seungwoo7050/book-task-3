# 개발 타임라인: E-async-jobs-lab

이 문서는 소스 코드에서 드러나지 않는 개발 과정—환경 설정, 패키지 설치,
Docker 구성, 마이그레이션, 디버깅 명령—을 시간순으로 기록한다.

---

## Phase 1: 프로젝트 초기화

```bash
mkdir -p labs/E-async-jobs-lab/fastapi && cd labs/E-async-jobs-lab/fastapi

# pyproject.toml 생성 (name: e-async-jobs-lab-fastapi)
# 핵심 의존성: fastapi, sqlalchemy, pydantic-settings, celery>=5.4, redis
# dev 의존성: pytest, pytest-asyncio, httpx, ruff

python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

Celery 5.4를 명시적으로 의존성에 추가해야 했다.
기존 A~D lab에는 없던 패키지이므로, pyproject.toml에 별도 항목으로 넣었다.

## Phase 2: Celery + Redis 설정

```bash
# app/core/config.py에 추가한 설정 필드:
#   celery_broker_url = "memory://"
#   celery_result_backend = "cache+memory://"
#   celery_task_always_eager = False
```

기본값을 `memory://`로 두어 `.env` 없이도 테스트가 돌아가게 했다.
Redis URL은 compose 환경의 `.env`에서 override된다.

```bash
# app/celery_app.py: Celery 인스턴스 생성
# app/tasks.py: deliver_notification 태스크 정의
```

## Phase 3: 모델과 마이그레이션

```bash
# SQLAlchemy 모델 정의
#   NotificationJob: id, idempotency_key(unique), recipient, subject, body, status, attempt_count
#   OutboxEvent: id, job_id(FK), event_type, status, created_at

# Alembic 초기화
alembic init alembic
# alembic.ini의 sqlalchemy.url을 env.py에서 Settings로 대체

alembic revision --autogenerate -m "add notification_job and outbox_event tables"
alembic upgrade head
```

`idempotency_key`에 unique constraint를 걸어야 멱등성이 DB 수준에서 보장된다.
인덱스를 빠뜨리면 동시 요청 시 duplicate가 발생한다.

## Phase 4: 서비스 레이어 구현

핵심 로직 순서:
1. `enqueue_notification`: idempotency_key로 기존 job lookup
   - 있으면 → 기존 job 반환
   - 없으면 → NotificationJob + OutboxEvent를 같은 session에서 생성, commit
2. `process_event`: pending outbox event를 꺼내서
   - recipient이 `retry@`로 시작하면 job.status = `retrying`, attempt_count += 1
   - 그 외에는 job.status = `sent`, attempt_count += 1
   - event.status = `done`

```python
# 핵심: job과 event가 같은 트랜잭션에 들어가야 outbox 패턴이 성립한다
session.add(job)
session.add(outbox_event)
session.commit()
```

## Phase 5: API 라우트

```bash
# POST /api/v1/notifications
#   - Header: Idempotency-Key (필수)
#   - Body: recipient, subject, body
#   - 201 Created + job 정보

# POST /api/v1/outbox/drain
#   - pending event 전체 처리
#   - 200 OK + 처리 결과

# GET /api/v1/notifications/{id}
#   - job 조회
```

## Phase 6: Docker Compose 구성

```yaml
# compose.yaml — 4개 서비스
services:
  api:       # FastAPI, 포트 8003:8000
  worker:    # Celery worker, 같은 이미지
  postgres:  # PostgreSQL 16, 포트 5435:5432
  redis:     # Redis 7, 포트 6380:6379
```

worker 서비스가 추가된 것이 이전 lab들과의 차이점이다.
같은 Docker image를 쓰되, CMD만 `celery -A app.celery_app worker`로 바꾼다.

```bash
docker compose up --build -d
docker compose logs -f worker   # 워커 로그 확인
```

## Phase 7: 테스트 작성

```bash
# conftest.py
#   - monkeypatch로 DATABASE_URL을 SQLite로 override
#   - celery_app.conf.task_always_eager = True 설정
#   - memory:// broker/backend로 override

# test_jobs.py
#   test_idempotent_enqueue: 같은 key로 2번 POST → 같은 job_id 반환
#   test_retrying_job: retry@prefix → 첫 drain 후 retrying → 두 번째 drain 후 sent

pytest -q
```

eager 모드에서 `task_always_eager=True`로 설정하면
worker 프로세스 없이 같은 프로세스에서 태스크가 실행된다.
CI에서 Redis 없이 테스트할 수 있는 핵심 설정이다.

## Phase 8: 검증

```bash
make lint     # ruff check app tests
make test     # pytest -q
make smoke    # smoke test (선택)

# Compose 검증
docker compose up --build -d
curl http://localhost:8003/api/v1/notifications -X POST \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: test-key-001" \
  -d '{"recipient":"user@example.com","subject":"hello","body":"world"}'

curl http://localhost:8003/api/v1/outbox/drain -X POST
curl http://localhost:8003/api/v1/notifications/1
docker compose down
```

---

## 타임라인 요약

| 단계 | 핵심 산출물 |
|------|-------------|
| 초기화 | pyproject.toml + celery 의존성 |
| Celery 설정 | celery_app.py, tasks.py, config 필드 |
| 모델 | NotificationJob, OutboxEvent, Alembic migration |
| 서비스 | enqueue_notification, process_event |
| API | POST /notifications, POST /outbox/drain, GET /notifications/{id} |
| Compose | api + worker + postgres + redis (4 서비스) |
| 테스트 | idempotent enqueue, retry 상태 전이 |
| 검증 | lint, test, compose curl 검증 |
