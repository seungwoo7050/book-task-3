# C-authorization-lab evidence ledger

## 독립 프로젝트 판정

- 판정: 처리 대상
- 이유: [`README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/README.md) 와 `problem/README.md` 가 인증을 의도적으로 제외 범위로 밀어내고, 통합 테스트가 invite 승격과 outsider 차단을 직접 고정한다.
- 프로젝트 질문: 인증 메커니즘을 거의 비워 둔 상태에서도 인가 규칙을 standalone으로 설명할 수 있는가.
- 복원 방식: 기존 `blog/` 본문은 근거에서 제외하고, `problem/README`, source code, tests, 실제 재실행 CLI만 사용했다.

## 근거 인벤토리

- [`problem/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/problem/README.md)
- [`docs/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/docs/README.md)
- [`fastapi/README.md`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/README.md)
- [`app/api/deps.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/deps.py)
- [`app/api/v1/routes/authorization.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py)
- [`app/domain/services/authorization.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/domain/services/authorization.py)
- [`app/repositories/authorization_repository.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/repositories/authorization_repository.py)
- [`app/db/models/authorization.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/db/models/authorization.py)
- [`app/schemas/authorization.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/schemas/authorization.py)
- [`tests/integration/test_authorization_flows.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py)
- [`tests/smoke.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/tests/smoke.py)

## Chronology ledger

| 순서 | 당시 목표 | 변경 단위 | 실제로 확인한 것 | CLI | 검증 신호 | 다음으로 넘어간 이유 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 인증을 비우고도 인가가 설명 가능한지 먼저 판정한다 | `README.md`, `problem/README.md`, `api/deps.py` | actor 입력을 `X-User-Id` 헤더 하나로 축소하고, 로그인 시스템은 범위 밖으로 밀어냈다 | `rg -n 'X-User-Id' backend-fastapi/labs/C-authorization-lab/fastapi/app backend-fastapi/labs/C-authorization-lab/fastapi/tests` | 이 랩의 중심은 로그인 방식이 아니라 actor identity와 role threshold다 | 이제 actor가 어떤 상태 전이를 일으키는지 route/service로 내려가야 한다 |
| 2 | invitation lifecycle이 authorization의 중심인지 확인한다 | `authorization.py`, `authorization.py` service, repository, models | invite 생성, 수락, 거절, role change, document create/read가 하나의 surface로 묶여 있다 | `rg -n 'accepted|declined|INVITE_EMAIL_MISMATCH|MEMBERSHIP_NOT_FOUND|FORBIDDEN' backend-fastapi/labs/C-authorization-lab/fastapi/app backend-fastapi/labs/C-authorization-lab/fastapi/tests` | invitation은 단순 CRUD가 아니라 actor와 email이 맞아야만 상태를 바꿀 수 있는 transition이다 | 다음은 역할 임계값이 실제 403/200 경계로 어떻게 보이는지 테스트에서 확인한다 |
| 3 | role threshold와 소유권 차이를 실제 요청 순서로 고정한다 | `AuthorizationService`, `test_authorization_flows.py` | `ROLE_ORDER`가 viewer/member/admin/owner 임계값을 정하고, owner만 role change를 할 수 있다 | `rg -n 'ROLE_ORDER|owner|viewer|member' backend-fastapi/labs/C-authorization-lab/fastapi/app backend-fastapi/labs/C-authorization-lab/fastapi/tests` | viewer는 문서 생성에서 403, promote 뒤에는 200, outsider read는 403으로 고정된다 | 마지막으로 지금 셸에서 공식 검증 명령이 실제로 어떻게 깨지는지 확인한다 |
| 4 | 현재 재검증 상태를 최신 값으로 닫는다 | `Makefile`, `schemas/authorization.py`, `health.py`, `tests/smoke.py`, 현재 셸 환경 | 공식 `make` 진입점과 `PYTHONPATH` 보조 재실행 모두 즉시 통과하지는 않는다 | `make lint`<br>`make test`<br>`make smoke`<br>`PYTHONPATH=. pytest`<br>`PYTHONPATH=. python -m tests.smoke` | `make lint`는 `health.py` E501, `make test`는 `No module named 'app'`, `make smoke`는 `No module named 'fastapi'`, 보조 재실행은 `email-validator` 부재에서 실패한다 | 규칙 설계와 현재 재현 환경의 간극을 함께 남겨야 문서 품질이 맞는다 |
