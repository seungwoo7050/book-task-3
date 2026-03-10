# 개발 타임라인

## 이 문서의 목적

- J 랩을 다시 열었을 때 “gateway가 무엇을 대신하고 무엇을 숨기는가”를 기준으로 재현 순서를 잡게 한다.
- gateway, internal service, websocket fan-out을 하나의 public flow로 다시 확인하게 한다.

## 1. 시작 위치를 고정한다

```bash
cd labs/J-edge-gateway-lab/fastapi
cp .env.example .env
```

- 이 랩의 외부 노출 포트는 `gateway=8013`, `identity-service=8121`, `workspace-service=8122`, `notification-service=8123`, `redis=6393`다.

## 2. 단위 검증을 먼저 통과시킨다

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHON="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python" \
make test
```

- gateway unit test, 각 서비스 unit test, top-level system test가 순서대로 실행된다.
- gateway가 edge 역할을 맡기 때문에 여기서는 service test와 top-level test를 함께 보는 편이 낫다.

## 3. Compose 통합 흐름을 확인한다

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHONPATH=. \
/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python -m pytest tests/test_system.py -q

PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHONPATH=. \
/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python -m tests.smoke
```

- system test는 public auth, workspace/invite 흐름, websocket 연결, notification-service 장애 후 recovery까지 확인한다.
- smoke는 gateway public health가 Compose에서 다시 올라오는지 확인한다.

## 4. 실제 재검증 메모

- 마지막 확인일: `2026-03-10`
- 확인한 항목: `make test`, `pytest tests/test_system.py -q`, `python -m tests.smoke`
- 메모: gateway dependency, project name, cleanup timeout 문제를 수정한 뒤 재검증했다.
