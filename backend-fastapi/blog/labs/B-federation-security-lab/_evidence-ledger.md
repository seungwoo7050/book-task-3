# B-federation-security-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README가 OIDC, TOTP, recovery code, audit log를 하나의 인증 보강 문제로 묶고, `tests/integration/test_google_callback.py`, `tests/integration/test_two_factor.py`, `tests/unit/test_token_rotation.py`가 각각 다른 실패 축을 검증한다.
- 프로젝트 질문: 외부 로그인과 보안 강화 기능을 기존 세션 모델 위에 붙일 때, 어떤 단계부터 추가 복잡성을 드러낼 것인가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/B-federation-security-lab/README.md`
- `labs/B-federation-security-lab/problem/README.md`
- `labs/B-federation-security-lab/docs/README.md`
- `labs/B-federation-security-lab/fastapi/README.md`
- `labs/B-federation-security-lab/fastapi/Makefile`
- `labs/B-federation-security-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/app/api/v1/routes/auth.py`
- `backend-fastapi/labs/B-federation-security-lab/fastapi/tests/integration/test_two_factor.py`
- `git log -- backend-fastapi/labs/B-federation-security-lab`

## 프로젝트 표면 요약
- 문제 요약: 이미 로컬 인증이 있는 서비스에 외부 로그인과 보안 강화 기능을 붙여야 한다고 가정합니다. 사용자는 Google 스타일 로그인으로 진입할 수 있어야 하고, 필요하면 2단계 인증과 recovery code를 사용할 수 있어야 합니다. 동시에 로그인 시도는 남용에 대비해 제한하고, 중요한 인증 이벤트는 기록해야 합니다. 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다. TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다. TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다. recovery code 재생성 및 소진 규칙이 있어야 합니다. 로그인 throttling과 audit log가 최소 수준으로라도 동작해야 합니다.
- 설계 질문: 외부 공급자 계정과 내부 사용자 계정을 어떻게 연결할 것인가 2FA를 로그인 흐름 어디에 끼워 넣을 것인가 recovery code는 왜 평문으로 두면 안 되는가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | 외부 로그인과 보안 강화 기능을 기존 로컬 인증과 분리해 설명 | README.md, problem/README.md, docs/README.md | Google 로그인만 추가하면 다음 단계로 넘어갈 수 있을 것 | OIDC, TOTP, recovery code, throttling, audit log를 같은 랩 surface로 묶음 | README의 `make run`, `docker compose up --build` | 문제 정의와 README가 provider link와 2FA를 동등한 성공 기준으로 둠 | README.md 문제 요약 / 핵심 설계 선택 | 외부 로그인은 편의 기능이 아니라 기존 세션 모델을 다시 검토하게 만드는 변화다 | OIDC callback을 내부 세션 발급과 연결 |
| 2 | Phase 2, 초기 구현 순서를 route/test 의존성으로 복원 | authorization-code callback을 내부 세션 발급의 중심으로 고정 | app/api/v1/routes/auth.py, app/domain/services/google_oidc.py | provider access token만 받으면 충분할 것 | signed state cookie, code verifier, id token 검증, 내부 user/session 연결을 callback에 집중 | `make test` | callback이 state cookie 부재를 바로 에러로 막고 user payload를 반환 | app/api/v1/routes/auth.py::google_callback | 외부 공급자 성공이 곧 내부 인증 성공은 아니다. 둘 사이엔 연결 계층이 하나 더 필요하다 | 2FA challenge를 로그인 후속 단계로 분리 |
| 3 | Phase 3, 테스트가 보안 단계 분리를 굳힘 | 2FA setup, confirm, verify, recovery code rotation을 별도 상태 전이로 고정 | tests/integration/test_two_factor.py, tests/unit/test_token_rotation.py | TOTP code 검증 한 번이면 2FA 설명이 끝날 것 | 재로그인 후 `me`가 401인 challenge 상태, recovery code 8개 발급, recovery login 성공까지 테스트화 | `make test` | 재로그인 직후 `GET /api/v1/auth/me` 401, recovery code 검증 후 `authenticated` | tests/integration/test_two_factor.py::test_two_factor_setup_and_recovery_code_login | 2FA는 인증 성공을 강화하는 기능이 아니라, 인증을 두 단계로 나누는 상태 기계다 | mock 기반 OIDC 경계를 문서로 고정 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | 실제 Google 없이도 OIDC surface와 2FA 흐름이 재현된다는 사실 확인 | docs/verification-report.md, fastapi/README.md, .github/workflows/labs-fastapi.yml | 문서만 있으면 mock 기반 검증 범위가 충분히 전달될 것 | compile, lint, test, smoke, Compose probe 결과와 PostgreSQL DB 이름 수정 메모를 남김 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/B-federation-security-lab/fastapi 8000` | 2026-03-09 기준 재검증 통과, DB 이름 불일치 수정 후 재실행 | docs/verification-report.md B-federation-security-lab 항목 | 외부 공급자 통합을 설명할 때도 mock 경로와 실제 서비스 경계를 분리해 써야 한다 | 인증에서 인가 규칙으로 초점을 옮기기 |
