# C-authorization-lab series map

이 시리즈는 인증을 거의 비워 둔 상태에서 인가만 따로 읽는다. 핵심은 "어떻게 로그인했는가"가 아니라, `X-User-Id`로 표현한 actor가 workspace membership, invitation status, role threshold를 기준으로 언제 403을 받아야 하는지 설명하는 일이다.

## 이 시리즈가 붙잡는 질문

- 인증을 단순 header actor 모델로 축소해도 인가 규칙을 흐리지 않고 설명할 수 있는가
- 역할과 소유권은 어디서 갈리고, 어느 규칙에서 다시 만나는가
- invitation lifecycle은 단순 CRUD가 아니라 어떤 상태 전이로 읽어야 하는가
- viewer, member, owner의 차이가 실제 문서 접근과 role change에 어떻게 반영되는가

## 왜 이 순서로 읽는가

1. `problem/README.md`와 상위 `README.md`로 이 랩이 일부러 인증을 범위 밖으로 밀어낸 이유를 먼저 확인한다.
2. `api/deps.py`와 `authorization.py`를 보며 actor 입력이 얼마나 단순하게 줄었는지 확인한다.
3. `AuthorizationService`와 `ROLE_ORDER`를 따라가며 invitation, membership, document 접근이 어떤 임계값으로 결정되는지 본다.
4. 통합 테스트를 보며 viewer가 거절당했다가 promote 뒤 허용되는 흐름과 outsider 차단 흐름을 같이 확인한다.
5. 마지막에 `make lint`, `make test`, `make smoke`와 보조 재실행 결과를 붙여 현재 셸 기준 재현 가능 상태를 확인한다.

## 근거로 사용한 자료

- `backend-fastapi/labs/C-authorization-lab/README.md`
- `backend-fastapi/labs/C-authorization-lab/problem/README.md`
- `backend-fastapi/labs/C-authorization-lab/docs/README.md`
- `backend-fastapi/labs/C-authorization-lab/fastapi/README.md`
- `backend-fastapi/labs/C-authorization-lab/fastapi/Makefile`
- `backend-fastapi/labs/C-authorization-lab/fastapi/app/api/deps.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/app/domain/services/authorization.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/app/repositories/authorization_repository.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/app/db/models/authorization.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/app/schemas/authorization.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/tests/smoke.py`

## 현재 검증 상태

- 2026-03-14 기준 `make lint`는 [`health.py`](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/v1/routes/health.py) 의 한 줄 길이 초과(`E501`) 때문에 실패했다.
- 같은 날짜 `make test`는 `ModuleNotFoundError: No module named 'app'`로 멈췄다.
- 같은 날짜 `make smoke`는 `python3`가 `/opt/homebrew/bin/python3`를 타면서 `ModuleNotFoundError: No module named 'fastapi'`로 실패했다.
- 보조 확인으로 `PYTHONPATH=. pytest`를 다시 돌리면 `EmailStr` schema import 단계에서 `email-validator` 미설치 오류로 멈춘다.
- `PYTHONPATH=. python -m tests.smoke`도 같은 `email-validator` 부재에서 실패한다.
- 즉 role/invite state machine은 코드와 테스트로 읽히지만, 현재 셸 기준 재검증 진입점은 그대로 통과하지 않는다.

## 현재 범위 밖

- 실제 로그인 시스템과 세션 관리
- 정책 엔진 같은 고급 외부 권한 시스템
- 조직 간 멀티테넌시 전체 설계

## 본문

- [10-development-timeline.md](10-development-timeline.md)
  - actor header, invitation lifecycle, role threshold, document permission이 어떻게 하나의 authorization surface로 묶이는지 구현 순서로 복원한다.
