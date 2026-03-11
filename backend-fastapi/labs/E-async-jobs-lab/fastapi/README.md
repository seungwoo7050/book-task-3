# E-async-jobs-lab FastAPI

이 문서는 E-async-jobs-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- notification enqueue API
- outbox handoff
- Celery worker 실행
- retry 상태 전이
- `/api/v1/health/live`, `/api/v1/health/ready`

## 빠른 실행

가장 빠른 로컬 확인:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make run
```

Compose 전체 확인:

```bash
cp .env.example .env
docker compose up --build
```

## 검증 명령

```bash
make lint
make test
make smoke
docker compose up --build
```

## 런타임 구성

- `api`: 호스트 `8003` 포트로 노출됩니다.
- `worker`: `celery -A app.workers.celery_app.celery_app worker --loglevel=INFO`로 시작합니다.
- `db`: PostgreSQL 16, 데이터베이스 이름은 `e_async_jobs_lab`입니다.
- `redis`: Redis 7을 `6380` 포트로 노출합니다.

## 실행 전에 알아둘 점

- `make run`은 기본 SQLite와 메모리 broker 설정으로 API shape를 빠르게 확인할 때 적합합니다.
- `.env.example`은 PostgreSQL, Redis, worker를 함께 올리는 Compose 기준 값입니다.
- Compose는 API와 worker를 같은 이미지로 띄우며, 둘 다 DB와 Redis health check를 기다립니다.
- 테스트와 로컬 실행은 비동기 작업 경계를 설명하는 데 초점을 둡니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
