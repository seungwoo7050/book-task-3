# 개발 타임라인

## 이 문서의 목적

- I 랩을 다시 열었을 때 “comment 저장부터 notification 생성까지 어디서 끊기는가”를 기준으로 재현 순서를 잡게 한다.
- relay와 consumer를 한 번에 보되, 인증 세부사항에 끌려가지 않게 한다.

## 1. 시작 위치를 고정한다

```bash
cd labs/I-event-integration-lab/fastapi
cp .env.example .env
```

- 이 랩의 외부 노출 포트는 `workspace-service=8012`, `notification-service=8112`, `redis=6392`다.
- `identity-service`와 `gateway`는 이 랩 범위에 없다.

## 2. 단위 검증을 먼저 통과시킨다

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHON="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python" \
make lint

PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHON="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python" \
make test
```

- `workspace-service` 테스트는 outbox row 생성까지 확인한다.
- `notification-service` 테스트는 consumer와 dedupe 저장을 확인한다.

## 3. Compose 통합 흐름을 확인한다

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHONPATH=. \
/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python -m pytest tests/test_system.py -q

PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHONPATH=. \
/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python -m tests.smoke
```

- system test는 workspace 생성, invite, project/task/comment, relay, consume 2회, notification 조회까지 확인한다.
- 핵심 검증 포인트는 “duplicate consume 이후에도 notification 수가 늘지 않는다”는 점이다.

## 4. 실제 재검증 메모

- 마지막 확인일: `2026-03-10`
- 확인한 항목: `make lint`, `make test`, `pytest tests/test_system.py -q`, `python -m tests.smoke`
- 메모: settings 누락, UUID claim, container dependency 문제를 수정한 뒤 재검증했다.
