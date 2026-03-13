# C-authorization-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: 프로젝트 README와 problem 문서가 로그인 시스템을 의도적으로 제외 범위로 밀어내고, `tests/integration/test_authorization_flows.py`가 역할 변화와 접근 실패를 직접 검증한다.
- 프로젝트 질문: 워크스페이스 초대, 역할 변경, 문서 접근 제어를 인증 메커니즘과 분리해도 설명 가능한가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/C-authorization-lab/README.md`
- `labs/C-authorization-lab/problem/README.md`
- `labs/C-authorization-lab/docs/README.md`
- `labs/C-authorization-lab/fastapi/README.md`
- `labs/C-authorization-lab/fastapi/Makefile`
- `labs/C-authorization-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/C-authorization-lab/fastapi/app/api/v1/routes/authorization.py`
- `backend-fastapi/labs/C-authorization-lab/fastapi/tests/integration/test_authorization_flows.py`
- `git log -- backend-fastapi/labs/C-authorization-lab`

## 프로젝트 표면 요약
- 문제 요약: 워크스페이스 기반 협업 서비스에서 "누가 무엇을 할 수 있는가"를 명확히 해야 합니다. 초대, 역할 변경, 소유권, 읽기/쓰기 가능 범위를 코드로 표현하고, 인증 자체와는 분리해서 설명 가능한 구조를 만들어야 합니다. 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다. 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다. 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다. owner와 일반 member의 차이가 실제 리소스 접근에 반영되어야 합니다. 인가 규칙을 서비스 계층에서 테스트할 수 있어야 합니다.
- 설계 질문: 역할과 소유권은 무엇이 다른가 초대 흐름에서 누가 상태를 바꿀 수 있는가 인가 규칙을 테스트하기 좋은 경계는 어디인가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | 인증 메커니즘을 빼고도 인가 규칙을 설명할 수 있는 구조 만들기 | README.md, problem/README.md, docs/README.md | 로그인 시스템이 없으면 인가 랩이 너무 추상적으로 보일 것 | header 기반 actor 모델로 인증을 단순화하고 역할/소유권 규칙을 전면에 둠 | README의 `make run` | README가 인증을 제외 범위로 밀고 membership, invitation, role change를 핵심으로 둠 | README.md 핵심 설계 선택 | 인가를 설명하려면 로그인보다 actor와 역할표가 먼저 보이는 편이 낫다 | 초대와 역할 변경 surface 구체화 |
| 2 | Phase 2, route/service/repository 의존성으로 복원 | workspace invitation lifecycle을 규칙 엔진처럼 다루기 | app/api/v1/routes/authorization.py, app/domain/services/authorization.py, app/repositories/authorization_repository.py | 역할 필드만 있으면 접근 제어도 함께 설명될 것 | create_invite, accept_invite, decline_invite, change_role, create_document, get_document를 한 route surface로 배치 | `make test` | authorization route가 user/workspace/invite/document를 전부 아우름 | app/api/v1/routes/authorization.py::create_invite | 인가 규칙은 리소스 읽기/쓰기보다 invitation lifecycle을 먼저 고정해야 흔들리지 않는다 | 역할 변경 전후의 실제 차이를 테스트로 고정 |
| 3 | Phase 3, 테스트가 규칙 전환점을 명확히 만듦 | viewer->member 승격과 outsider 차단을 실제 요청 순서로 고정 | tests/integration/test_authorization_flows.py | 허용 경로만 확인해도 역할표를 설명할 수 있을 것 | viewer가 문서 생성에서 403을 받고, promote 뒤에는 200이 되는 흐름과 decline/outsider 403 경로를 테스트화 | `make test` | 초대 수락 전후, 역할 변경 전후, outsider 읽기 실패가 모두 테스트에 존재 | tests/integration/test_authorization_flows.py::test_invite_accept_promote_and_document_permissions | 인가 글은 허용 규칙보다 '언제 403이 나와야 하는가'를 보여줄 때 설득력이 커진다 | 실행/재검증 표면 정리 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | 인가 규칙이 독립 워크스페이스로 재실행 가능하다는 사실을 닫기 | docs/verification-report.md, fastapi/README.md, .github/workflows/labs-fastapi.yml | 역할표만 문서화하면 충분히 이해될 것 | compile, lint, test, smoke, Compose probe 결과를 남기고 로컬 실행용 스키마 자동 초기화 메모를 기록 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh labs/C-authorization-lab/fastapi 8001` | 2026-03-09 기준 재검증 통과, 앱 시작 시 스키마 자동 초기화 메모 존재 | docs/verification-report.md C-authorization-lab 항목 | 인가 실습도 결국 DB 스키마와 HTTP surface가 살아 있어야 독립 프로젝트가 된다 | 데이터 API 설계로 초점 이동 |
