# C-authorization-lab structure plan

## 한 줄 약속

- 인증을 거의 비워 둔 상태에서도 invite, membership, role threshold만으로 인가 규칙이 얼마나 선명해질 수 있는지 보여 준다.

## 독자 질문

- 왜 이 랩은 로그인 방식 대신 `X-User-Id` actor 모델을 먼저 고정하는가
- invitation lifecycle은 단순 CRUD가 아니라 어떤 authorization 상태 전이인가
- `viewer`, `member`, `owner` 차이는 어느 요청에서 403과 200으로 갈리는가
- owner-only role change는 일반 RBAC과 무엇이 다른가
- 현재 문서에 적힌 검증 명령은 지금 셸에서 그대로 재현되는가

## 이번 Todo의 작성 원칙

- 다른 lab 문장이나 구조를 가져오지 않는다.
- 기존 `blog/` 본문은 사실 근거로 사용하지 않는다.
- `problem/README`, source code, tests, 실제 재실행 CLI만으로 서사를 복원한다.
- role 규칙의 선명함과 현재 import/dependency drift를 둘 다 숨기지 않는다.

## 글 흐름

1. `X-User-Id` actor 모델부터 열어 인증이 왜 의도적으로 축소됐는지 고정한다.
2. invitation 생성, 수락, 거절을 authorization surface의 중심 상태 전이로 읽는다.
3. `ROLE_ORDER`와 owner-only role change를 따라가며 권한 임계값을 서비스 계층에서 설명한다.
4. 통합 테스트로 viewer의 403, promote 이후 200, outsider의 403 경계를 회귀선처럼 고정한다.
5. 오늘 다시 돌린 CLI 결과로 현재 재현 가능 상태를 닫는다.

## Evidence anchor

- 주 코드 앵커: [AuthorizationService](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/domain/services/authorization.py)
- 보조 코드 앵커: [authorization.py route](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py), [authorization_repository.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/repositories/authorization_repository.py)
- 입력 경계 앵커: [deps.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/api/deps.py), [authorization.py schema](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/app/schemas/authorization.py)
- 테스트 앵커: [test_authorization_flows.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py)
- CLI 앵커: `make lint`, `make test`, `make smoke`, `PYTHONPATH=. pytest`, `PYTHONPATH=. python -m tests.smoke`

## 끝에서 남겨야 할 문장

- 이 랩의 강점은 인증 복잡도를 걷어낸 뒤에도 invite, membership, role threshold, owner 권한이 하나의 authorization surface로 또렷하게 읽힌다는 점이다.
- 이 랩의 현재 약점은 공식 검증 진입점이 2026-03-14 셸에서는 `app` path, `fastapi`, `email-validator` 문제로 바로 닫히지 않는다는 점이다.
- 다음 랩인 `D-data-api-lab`은 권한 규칙을 이미 분리해 둔 상태에서 데이터 API 일관성과 저장 흐름으로 초점을 옮기는 비교 대상으로 연결한다.
