# A-auth-lab evidence ledger

## 독립 프로젝트 판정

- 판정: 처리 대상
- 이유: [`README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/README.md) 가 문제 범위를 독립적으로 설명하고, [`fastapi/Makefile`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/Makefile) 와 통합 테스트가 재검증 진입점을 따로 가진다.
- 프로젝트 질문: 로컬 계정 인증을 어디까지 "기본 인증 흐름"으로 볼 것인가. 로그인까지만인가, 아니면 이메일 검증, 회복, refresh rotation, CSRF까지인가.
- 복원 방식: 기존 `blog/` 본문은 근거에서 제외하고, `problem/README`, source code, tests, 실제 재실행 CLI만 사용했다.

## 근거 인벤토리

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/problem/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/docs/README.md)
- [`fastapi/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/README.md)
- [`app/api/v1/routes/auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py)
- [`app/api/deps.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/deps.py)
- [`app/core/security.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/core/security.py)
- [`app/domain/services/auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/domain/services/auth.py)
- [`app/db/models/auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/db/models/auth.py)
- [`tests/integration/test_local_auth.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py)
- [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/tests/smoke.py)

## Chronology ledger

| 순서 | 당시 목표 | 변경 단위 | 실제로 확인한 것 | CLI | 검증 신호 | 다음으로 넘어간 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | auth surface가 로그인만으로 끝나는지 먼저 판정한다 | `problem/README.md`, `README.md`, `auth.py` | route 목록에 `verify-email`, `password-reset`, `token/refresh`, `logout`까지 모두 있어 범위가 이미 넓다 | `rg -n '"/register"|"verify-email"|password-reset|"/token/refresh"|"/logout"' backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py` | 공개 표면만 봐도 이 랩의 중심이 "계정 생애주기" 쪽으로 이동해 있다 | 공개 API만으로는 왜 rotation이 필요한지 설명이 부족해서 서비스 계층으로 내려간다 |
| 2 | refresh rotation이 정말 핵심 경계인지 확인한다 | `auth.py`, `auth.py` service, `models/auth.py` | `family_id`, `parent_token_id`, `reuse_detected_at`와 family revoke 로직이 따로 존재한다 | `rg -n 'family_id|parent_token_id|reuse_detected_at|REFRESH_TOKEN_REUSED|auth.refresh.reuse_detected' backend-fastapi/labs/A-auth-lab/fastapi/app/domain/services/auth.py backend-fastapi/labs/A-auth-lab/fastapi/app/db/models/auth.py backend-fastapi/labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py` | refresh는 재발급 기능이 아니라 탈취 감지 규칙으로 읽혀야 한다 | token family만으로는 cookie 기반 요청 보호가 설명되지 않아 CSRF 실패면을 본다 |
| 3 | cookie 인증에서 CSRF를 어디서 자르는지 확인한다 | `api/deps.py`, `core/security.py`, 통합 테스트 | `require_csrf`와 `validate_csrf`가 refresh/logout에 직접 붙고, 테스트가 403 `CSRF_VALIDATION_FAILED`를 고정한다 | `rg -n 'require_csrf|validate_csrf|CSRF_VALIDATION_FAILED|csrf_token' backend-fastapi/labs/A-auth-lab/fastapi/app/api/deps.py backend-fastapi/labs/A-auth-lab/fastapi/app/core/security.py backend-fastapi/labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py` | 회전 규칙과 CSRF 규칙이 같은 실패 코드로 섞이지 않고 분리된다 | 마지막으로 문서에 적힌 검증 명령이 지금 셸에서 실제로 재현되는지 확인한다 |
| 4 | 현재 재검증 상태를 최신 값으로 닫는다 | `Makefile`, `tests/smoke.py`, 현재 셸 환경 | 공식 `make` 진입점과 보조 `PYTHONPATH` 재실행 모두 즉시 통과하지는 않는다 | `make lint`<br>`make test`<br>`make smoke`<br>`PYTHONPATH=. pytest`<br>`PYTHONPATH=. python -m tests.smoke` | `make lint`는 `health.py` E501, `make test`는 `No module named 'app'`, `make smoke`는 `No module named 'fastapi'`, 보조 재실행은 `No module named 'argon2'` | 구현 설명은 가능하지만 재현 환경은 흔들린다는 사실까지 문서에 남겨야 현재 품질이 맞는다 |
