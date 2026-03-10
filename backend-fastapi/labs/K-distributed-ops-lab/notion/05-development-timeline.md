# 개발 타임라인

## 이 문서의 목적

- K 랩을 다시 열었을 때 “무엇을 볼 수 있어야 운영 가능하다고 말할 수 있나”를 기준으로 재현 순서를 잡게 한다.
- health, logs, metrics, target shape 문서를 도메인 흐름 위에서 같이 확인하게 한다.

## 1. 시작 위치를 고정한다

```bash
cd labs/K-distributed-ops-lab/fastapi
cp .env.example .env
```

- 이 랩의 외부 노출 포트는 `gateway=8014`, `identity-service=8131`, `workspace-service=8132`, `notification-service=8133`, `redis=6394`다.

## 2. 단위 및 통합 검증을 순서대로 본다

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHON="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python" \
make test
```

- gateway와 각 서비스 unit test가 먼저 돈다.
- 이후 top-level system test가 gateway 기준 public flow와 recovery를 확인한다.

## 3. 운영성 확인 루프를 다시 돌린다

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHONPATH=. \
/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python -m tests.smoke
```

- smoke는 Compose 부팅, gateway public health, 내부 서비스 healthcheck를 다시 확인한다.
- 이후 [../docs/aws-deployment.md](../docs/aws-deployment.md)를 읽고 target shape 문서가 실제 배포 완료 주장이 아니라는 점을 다시 확인한다.

## 4. 실제 재검증 메모

- 마지막 확인일: `2026-03-10`
- 확인한 항목: `make test`, `python -m tests.smoke`
- 메모: gateway/workspace dependency, project name, cleanup timeout 보정 후 재검증했다.
