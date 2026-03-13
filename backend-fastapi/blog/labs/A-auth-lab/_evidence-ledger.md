# A-auth-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: 프로젝트 README가 문제 범위를 단독으로 설명하고, `fastapi/Makefile`, `compose.yaml`, `tests/integration/test_local_auth.py`가 검증 진입점을 스스로 가진다.
- 프로젝트 질문: 회원가입과 로그인만 만드는 대신, 세션 회전과 계정 회복까지 한 묶음으로 어디까지 설명할 것인가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/A-auth-lab/README.md`
- `labs/A-auth-lab/problem/README.md`
- `labs/A-auth-lab/docs/README.md`
- `labs/A-auth-lab/fastapi/README.md`
- `labs/A-auth-lab/fastapi/Makefile`
- `labs/A-auth-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/A-auth-lab/fastapi/app/api/v1/routes/auth.py`
- `backend-fastapi/labs/A-auth-lab/fastapi/tests/integration/test_local_auth.py`
- `git log -- backend-fastapi/labs/A-auth-lab`

## 프로젝트 표면 요약
- 문제 요약: 사용자는 회원가입하고, 이메일을 검증하고, 로그인하고, 필요하면 비밀번호를 재설정할 수 있어야 합니다. 인증이 끝난 뒤에도 세션 유지와 상태 변경 요청 보호를 함께 설명할 수 있어야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: 회원가입과 로그인 흐름이 분리되어 설명 가능해야 합니다. 이메일 검증과 비밀번호 재설정 토큰 발급/소비가 동작해야 합니다. refresh token rotation이 왜 필요한지 코드와 문서로 설명할 수 있어야 합니다. cookie 인증 요청에 CSRF 방어가 함께 붙어야 합니다.
- 설계 질문: access token과 refresh token을 왜 분리하는가 이메일 검증과 비밀번호 재설정을 같은 토큰 계열 문제로 어디까지 묶을 수 있는가 cookie 인증에서 CSRF를 어디에서 차단해야 하는가
- 실제 검증 surface: cd fastapi make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | 로컬 계정 인증에서 어떤 상태 전이를 한 프로젝트 안에 둘지 정리 | README.md, problem/README.md, app/api/v1/routes/auth.py | 회원가입과 로그인만 구현해도 인증 랩으로 충분할 것 | verify_email, password_reset, refresh_token, logout route를 한 surface로 묶음 | README 기준 `make run`, `docker compose up --build` | auth route에 register/login/me 뿐 아니라 회복·회전 endpoint가 함께 존재 | app/api/v1/routes/auth.py::refresh_token | 인증 랩의 중심은 가입보다 세션의 장기 수명과 회복 경계에 가깝다 | cookie 기반 요청 보호를 어디에 둘지 정리 |
| 2 | Phase 2, 초기 구현 순서를 파일 의존성으로 복원 | refresh token reuse와 CSRF를 코드에서 분리해 설명 | app/core/security.py, app/domain/services/auth.py, app/repositories/auth_repository.py | refresh 재발급만 있으면 세션 갱신 설명이 끝날 것 | token family 회전, reuse 탐지, CSRF header 검증을 서비스/보안 계층에 배치 | `make test` | 401 `REFRESH_TOKEN_REUSED`, 403 `CSRF_VALIDATION_FAILED`를 테스트가 기대 | tests/integration/test_local_auth.py::test_local_login_refresh_rotation_and_logout | rotation은 UX 기능이 아니라 탈취 감지 장치다 | 비밀번호 재설정과 메일 검증 토큰을 회복 흐름으로 묶기 |
| 3 | Phase 3, 2026-03-10 docs/verification 정리와 함께 재구성 | 로컬 메일함과 공격자 클라이언트를 포함한 검증 흐름 고정 | tests/integration/test_local_auth.py, fastapi/README.md | 정상 플로우 테스트만 있으면 인증 설명에 충분할 것 | attacker TestClient, mailbox token helper, password reset 재로그인 검증 추가 | README의 `make test`, `make smoke` | 회전 재사용, 비밀번호 변경 후 옛 비밀번호 로그인 실패가 모두 명시됨 | tests/integration/test_local_auth.py::_latest_mail_token | 회복 흐름은 happy path보다 공격 경로를 같이 보여줄 때 더 설명력이 생긴다 | 실제 재실행 기록과 연결 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | 문서에 적힌 명령이 실제로 다시 실행됐음을 닫기 | docs/verification-report.md, .github/workflows/labs-fastapi.yml, tools/compose_probe.sh | README 명령만 있으면 충분히 검증되었다고 읽힐 것 | compile, lint, test, smoke, compose live/ready probe까지 실제 결과를 보고서에 남김 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/A-auth-lab/fastapi 8000` | 2026-03-09 기준 compile/lint/test/smoke/Compose probe 통과 | docs/verification-report.md A-auth-lab 항목 | 인증 랩도 마지막엔 HTTP surface가 살아 있는지 별도 probe가 필요하다 | 외부 로그인과 2FA를 붙이는 다음 랩으로 이동 |
