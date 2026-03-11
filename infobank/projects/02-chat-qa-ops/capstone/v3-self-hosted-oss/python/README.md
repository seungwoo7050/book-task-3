# Python 백엔드

이 디렉터리는 `v3-self-hosted-oss`의 FastAPI API, worker, CLI, SQLAlchemy 모델, pytest 회귀셋을 담는다.

## 제품 범위

- 단일 관리자 인증
- dataset JSONL import
- knowledge base ZIP import
- evaluation job queue
- run 단위 dashboard/session review API
- 선택형 provider chain / Langfuse 준비 경로

## 실행 명령

```bash
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make gate-all
```

개별 실행:

```bash
UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
UV_PYTHON=python3.12 PYTHONPATH=backend/src uv run python -m cli.main worker
```

PostgreSQL smoke 검증:

```bash
UV_PYTHON=python3.12 make smoke-postgres
```
