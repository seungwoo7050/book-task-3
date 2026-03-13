# workspace-backend Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: capstone README와 problem 문서가 랩들의 단순 합이 아니라 협업형 SaaS 도메인으로 재조합된 범위를 설명하고, `tests/integration/test_capstone.py`가 로컬/Google, invite, comment, drain, websocket을 한 흐름으로 묶는다.
- 프로젝트 질문: 인증, 인가, 데이터 API, 알림, 실시간 전달을 하나의 제품형 구조로 합칠 때 무엇을 다시 설계해야 하는가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `capstone/workspace-backend/README.md`
- `capstone/workspace-backend/problem/README.md`
- `capstone/workspace-backend/docs/README.md`
- `capstone/workspace-backend/fastapi/README.md`
- `capstone/workspace-backend/fastapi/Makefile`
- `capstone/workspace-backend/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/capstone/workspace-backend/fastapi/app/api/v1/routes/platform.py`
- `backend-fastapi/capstone/workspace-backend/fastapi/tests/integration/test_capstone.py`
- `git log -- backend-fastapi/capstone/workspace-backend`

## 프로젝트 표면 요약
- 문제 요약: 개별 랩으로 연습한 인증, 인가, 데이터 API, 비동기 알림, 실시간 전달을 하나의 협업형 SaaS 백엔드로 다시 조합합니다. 목표는 기능을 많이 붙이는 것이 아니라, 여러 경계를 함께 설명할 수 있는 통합 구조를 만드는 것입니다. 로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명 가능해야 합니다. 워크스페이스 멤버십과 역할이 프로젝트/태스크/댓글 API와 연결되어야 합니다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: 로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명 가능해야 합니다. 워크스페이스 멤버십과 역할이 프로젝트/태스크/댓글 API와 연결되어야 합니다. 알림 생성이 큐와 실시간 전달로 이어지는 흐름이 보여야 합니다. 개별 랩의 개념이 capstone에서 어떻게 다시 조합되었는지 문서로 설명할 수 있어야 합니다.
- 설계 질문: 인증, 인가, 데이터 API, 알림 전달이 어디서 만나고 어디서 분리되는가 랩 코드를 재사용하지 않고 다시 구현한 이유는 무엇인가 협업형 도메인에서 큐와 실시간 전달을 어떤 순서로 결합했는가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-11 89dc218 feat: add new project in fastapi (MSA)
- 2026-03-10 a3edce2 docs: enhance backend-fastapi
- 2026-03-09 7813150 docs(notion): front-react, backend-fastapi
- 2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-09 add project commit 73372bd를 기준으로 복원 | 분리 학습한 인증/인가/데이터/알림을 하나의 SaaS 도메인으로 조합 | README.md, problem/README.md, docs/README.md | 랩 코드를 그대로 합치면 capstone도 자연스럽게 완성될 것 | 공용 패키지 추출 대신 auth + platform 두 surface로 다시 구현하고 협업 도메인에 맞춤 | README의 `make run`, `docker compose up --build` | README가 로컬/Google 로그인, workspace membership, project/task/comment, queued notification, realtime delivery를 한 답으로 설명 | README.md 내 답 / 핵심 설계 선택 | capstone은 랩의 집합이 아니라, 경계들이 같은 도메인에서 어떻게 맞물리는지 다시 설계하는 작업이다 | platform route에 협업 흐름 집약 |
| 2 | Phase 2, route/service/repository 의존성으로 복원 | 협업형 SaaS의 주 흐름을 auth와 platform 두 surface로 정리 | app/api/v1/routes/auth.py, app/api/v1/routes/platform.py, app/domain/services/platform.py | 각 랩의 route 이름을 그대로 가져오면 충분할 것 | workspace, invite, project, task, comment, drain_notifications, heartbeat, presence, notifications_ws를 `platform.py`에 집중 | `make test` | `platform.py`가 댓글 생성부터 drain, presence, websocket까지 모두 가진다 | app/api/v1/routes/platform.py::create_comment | 통합 구조에서는 댓글 같은 도메인 이벤트가 비동기 알림과 실시간 전달의 중심 연결점이 된다 | 조합된 흐름을 통합 테스트로 고정 |
| 3 | Phase 3, 통합 테스트가 조합 순서를 고정 | 로컬 로그인과 Google 협업자 흐름, 초대, websocket notification을 한 번에 검증 | tests/integration/test_capstone.py | 단일 기능 테스트를 모두 통과시키면 capstone도 설명될 것 | owner local auth, collaborator Google login, invite accept, project/task/comment, notification drain, websocket 수신을 한 시나리오로 묶음 | `make test` | Google 로그인한 collaborator가 websocket에서 새 댓글 알림을 받음 | tests/integration/test_capstone.py::test_local_auth_workspace_flow_and_google_member_notification | 통합 프로젝트는 개별 기능의 유무보다 한 사용자의 행위가 다른 사용자의 알림으로 이어지는 순서를 보여줘야 한다 | 실제 재실행 기준선 확정 |
| 4 | 2026-03-09 재검증 + 2026-03-11 track polish | 단일 백엔드 기준선으로서 재실행 가능 상태를 확인 | docs/verification-report.md, fastapi/README.md, .github/workflows/labs-fastapi.yml | capstone은 복잡하니 문서만으로도 충분히 설명될 것 | compile, lint, test, smoke, Compose probe를 실제로 다시 돌리고 로컬 스키마 자동 초기화 메모를 남김 | `python3 -m compileall app tests`, `make lint`, `make test`, `make smoke`, `./tools/compose_probe.sh capstone/workspace-backend/fastapi 8010` | 2026-03-09 기준 재검증 통과, 앱 시작 시 스키마 자동 초기화 기록 | docs/verification-report.md workspace-backend 항목 | capstone도 결국 검증 surface가 단일 랩과 같은 단순한 명령으로 닫혀야 계속 비교 기준선이 된다 | MSA 재분해판과 비교 |
