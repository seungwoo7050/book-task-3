# 개발 타임라인

## 이 문서의 목적

- H 랩을 다시 열었을 때 “토큰 발급 후 첫 도메인 동작이 어디서 검증되나”를 바로 찾게 한다.
- 서비스 경계, DB ownership, Compose 부팅 순서를 한 번에 재현하게 한다.

## 1. 시작 위치를 고정한다

```bash
cd labs/H-service-boundary-lab/fastapi
cp .env.example .env
```

- 이 랩의 외부 노출 포트는 `workspace-service=8011`, `identity-service=8111`이다.
- Redis나 gateway는 이 랩 범위에 포함하지 않는다.

## 2. 가장 빠른 단위 검증 경로

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHON="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python" \
make lint

PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHON="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python" \
make test
```

- `identity-service`와 `workspace-service` 단위 테스트가 먼저 통과해야 한다.
- 여기서 깨지면 claim shape나 settings 누락부터 확인하는 편이 빠르다.

## 3. Compose 통합 흐름을 확인한다

```bash
PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHONPATH=. \
/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python -m pytest tests/test_system.py -q

PATH="/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin:$PATH" \
PYTHONPATH=. \
/Users/woopinbell/work/book-task-3/backend-fastapi/.venv/bin/python -m tests.smoke
```

- system test는 `identity-service`에서 회원가입, 이메일 검증, 로그인 후 `workspace-service`에서 워크스페이스 생성을 확인한다.
- smoke는 Compose 부팅과 health 응답을 다시 확인한다.

## 4. 실제 재검증 메모

- 마지막 확인일: `2026-03-10`
- 확인한 항목: `make lint`, `make test`, `pytest tests/test_system.py -q`, `python -m tests.smoke`
- 메모: service container 의존성과 Compose project name 충돌을 수정한 뒤 재검증했다.
