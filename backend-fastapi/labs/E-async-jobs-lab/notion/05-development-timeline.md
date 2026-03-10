# 개발 타임라인

## 이 문서의 목적

- 비동기 랩을 다시 볼 때 enqueue, outbox, worker, retry가 어느 순서로 움직이는지 재현 가능한 경로로 정리한다.
- API만 띄우는 빠른 확인과 worker까지 포함한 전체 경로를 분리해서 적는다.

## 1. 시작 위치를 고정한다

```bash
cd labs/E-async-jobs-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
```

- 기본 설정은 SQLite와 메모리 broker/backend를 사용한다.
- 다만 `celery_task_always_eager` 기본값이 `false`라서, 실제 `/api/v1/jobs/outbox/drain` 성공 경로는 worker가 있는 Compose에서 보는 편이 안전하다.
- `.env.example`을 복사하면 PostgreSQL + Redis 경로로 전환된다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_async_jobs.py -q
make smoke
```

- 테스트는 `Idempotency-Key` 중복 요청이 같은 job id를 재사용하는지, 첫 drain에서 `retrying`, 두 번째 drain에서 `sent`로 바뀌는지 확인한다.
- `make smoke`는 앱 부팅과 `/api/v1/health/live`만 확인한다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- 이 루프는 route shape와 service 계층 구조를 빠르게 읽을 때 좋다.
- drain까지 로컬에서 한 번에 보고 싶다면 셸에서 `export CELERY_TASK_ALWAYS_EAGER=true`를 한 뒤 `make run`을 다시 시작한다.

## 4. Compose로 worker까지 같이 띄운다

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
docker compose logs worker --tail=50
curl http://127.0.0.1:8003/api/v1/health/live
curl http://127.0.0.1:8003/api/v1/health/ready
```

- Compose에서는 API가 `8003`, PostgreSQL이 `5435`, Redis가 `6380` 포트로 노출된다.
- 이 랩은 `api`, `worker`, `db`, `redis` 네 서비스가 모두 떠야 “비동기 전달”이라는 이름에 맞는 그림이 나온다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 수동 비동기 흐름을 재현한다

첫 번째 job은 중복 요청이 같은 id를 재사용하는지 본다.

```bash
curl -X POST http://127.0.0.1:8003/api/v1/jobs/notifications \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: job-1' \
  -d '{"recipient":"team@example.com","subject":"Deploy finished"}'

curl -X POST http://127.0.0.1:8003/api/v1/jobs/notifications \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: job-1' \
  -d '{"recipient":"team@example.com","subject":"Deploy finished"}'
```

- 두 응답의 `id`가 같아야 한다.

이제 outbox를 drain하고 상태를 본다.

```bash
curl -X POST http://127.0.0.1:8003/api/v1/jobs/outbox/drain
curl http://127.0.0.1:8003/api/v1/jobs/notifications/<JOB_ID>
```

- 첫 번째 job의 상태는 `sent`여야 한다.

retry 경로는 의도적으로 한 번 실패하게 만든다.

```bash
curl -X POST http://127.0.0.1:8003/api/v1/jobs/notifications \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: job-2' \
  -d '{"recipient":"retry@example.com","subject":"Retry me"}'

curl -X POST http://127.0.0.1:8003/api/v1/jobs/outbox/drain
curl http://127.0.0.1:8003/api/v1/jobs/notifications/<RETRY_JOB_ID>

curl -X POST http://127.0.0.1:8003/api/v1/jobs/outbox/drain
curl http://127.0.0.1:8003/api/v1/jobs/notifications/<RETRY_JOB_ID>
```

- 첫 번째 조회는 `retrying`, 두 번째 조회는 `sent`와 `attempt_count = 2`여야 한다.

## 6. 막히면 먼저 확인할 것

- 두 번 enqueue했는데 id가 다르면 `Idempotency-Key` 헤더가 빠졌는지 먼저 본다.
- drain이 멈추면 `docker compose logs worker`에서 Celery worker가 살아 있는지 확인한다.
- retry 경로가 바로 `sent`가 되면 테스트에서 쓰는 `retry@example.com` 패턴을 그대로 사용했는지 확인한다.
