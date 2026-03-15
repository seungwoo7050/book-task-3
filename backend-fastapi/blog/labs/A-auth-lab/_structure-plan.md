# A-auth-lab structure plan

## 한 줄 약속

- 로컬 인증을 "로그인 API"가 아니라 token family, recovery, CSRF까지 포함한 세션 규칙으로 읽게 만든다.

## 독자 질문

- 로컬 계정 인증에서 어디까지를 기본 범위로 봐야 하는가
- refresh rotation은 왜 단순 재발급이 아니라 별도 보안 규칙인가
- recovery token과 session token은 어디서 갈라지고 어디서 닮아 있는가
- 현재 문서에 적힌 검증 명령은 지금 셸에서도 그대로 재현되는가

## 이번 Todo의 작성 원칙

- 다른 lab 문장이나 구조를 가져오지 않는다.
- 기존 `blog/` 본문은 사실 근거로 사용하지 않는다.
- `problem/README`, source code, tests, 실제 재실행 CLI만으로 서사를 복원한다.
- 현재 재검증 실패도 품질 정보로 취급하고 숨기지 않는다.

## 글 흐름

1. route surface를 먼저 열어 이 랩이 로그인보다 넓은 범위를 갖는다는 점을 고정한다.
2. refresh token family와 reuse detection을 세션의 중심 규칙으로 올린다.
3. CSRF와 cookie 인증을 별도 실패면으로 분리한다.
4. verify/reset token이 같은 저장소를 공유하는 recovery 구조를 설명한다.
5. 오늘 다시 돌린 CLI 결과로 재현 가능 상태를 닫는다.

## Evidence anchor

- 주 코드 앵커: [auth.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py)
- 보조 코드 앵커: [AuthService](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/domain/services/auth.py), [RefreshToken model](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/db/models/auth.py)
- 보안 앵커: [validate_csrf](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/core/security.py), [require_csrf](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/app/api/deps.py)
- 테스트 앵커: [test_local_auth.py](/Users/woopinbell/work/book-task-3/backend-fastapi/labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py)
- CLI 앵커: `make lint`, `make test`, `make smoke`, `PYTHONPATH=. pytest`, `PYTHONPATH=. python -m tests.smoke`

## 끝에서 남겨야 할 문장

- 이 랩의 강점은 token family, reuse detection, CSRF, recovery 흐름이 한 surface 안에서 선명하게 연결된다는 점이다.
- 이 랩의 현재 약점은 문서에 적힌 검증 진입점이 2026-03-14 셸에서는 그대로 재현되지 않는다는 점이다.
- 다음 랩인 `B-federation-security-lab`은 이 로컬 세션 경계 위에 외부 로그인과 추가 인증 단계를 얹는 비교 대상으로 연결한다.
