# H-service-boundary-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README와 problem 문서가 `identity-service`와 `workspace-service`의 DB ownership을 핵심 성공 기준으로 삼고, `compose.yaml`과 `tests/test_system.py`가 실제 runtime scope를 두 서비스로 제한한다.
- 프로젝트 질문: 단일 백엔드에서 자연스럽게 함께 있던 인증과 워크스페이스 도메인을 어디서 끊을 것인가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/H-service-boundary-lab/README.md`
- `labs/H-service-boundary-lab/problem/README.md`
- `labs/H-service-boundary-lab/docs/README.md`
- `labs/H-service-boundary-lab/fastapi/README.md`
- `labs/H-service-boundary-lab/fastapi/Makefile`
- `labs/H-service-boundary-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/H-service-boundary-lab/fastapi/compose.yaml`
- `backend-fastapi/labs/H-service-boundary-lab/fastapi/tests/test_system.py`
- `git log -- backend-fastapi/labs/H-service-boundary-lab`

## 프로젝트 표면 요약
- 문제 요약: 단일 백엔드에서 자연스럽게 함께 있던 인증과 워크스페이스 도메인을 처음으로 분리한다. 핵심 질문은 "어디서 경계를 끊어야 하며, 서비스가 서로의 DB를 읽지 않고도 동작할 수 있는가"이다. `identity-service`가 토큰을 발급한다. `workspace-service`가 그 토큰 claims만으로 workspace를 생성한다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: `identity-service`가 토큰을 발급한다. `workspace-service`가 그 토큰 claims만으로 workspace를 생성한다. 두 서비스가 각자 자기 DB만 읽고, cross-DB 조회를 하지 않는다.
- 설계 질문: 인증 서비스와 워크스페이스 서비스를 왜 분리하는가 어떤 데이터는 claim으로 넘기고 어떤 데이터는 넘기지 않는가 서비스별 DB ownership을 어디까지 강제할 것인가 공유 ORM 모델을 금지하면 무엇이 불편해지고 무엇이 명확해지는가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-11 89dc218 feat: add new project in fastapi (MSA)

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-11 add project commit 89dc218을 기준으로 복원 | 인증과 워크스페이스 도메인을 처음으로 서비스 경계로 나누기 | README.md, problem/README.md, docs/README.md | 서비스를 나누려면 gateway와 이벤트 브로커까지 한 번에 있어야 할 것 | 성공 기준을 `identity-service` token 발급, `workspace-service` claims 소비, cross-DB 조회 금지로 좁힘 | README의 `docker compose up --build` | 제외 범위가 gateway, event broker, websocket을 명시적으로 밀어냄 | problem/README.md 제외 범위 | 첫 서비스 분해에서는 기능 수보다 경계를 얼마나 좁게 정의하느냐가 더 중요하다 | runtime scope를 compose로 고정 |
| 2 | Phase 2, compose/runtime scope를 중심으로 복원 | 실행 가능한 MSA 최소 단위를 두 서비스로 제한 | fastapi/compose.yaml, fastapi/README.md | 폴더에 gateway나 notification-service가 있으면 그것도 이 랩의 핵심일 것 | runtime compose에는 identity-service와 workspace-service만 두고, 각자 자기 DB를 소유하게 구성 | `docker compose up --build` | compose.yaml이 8111/8011 포트의 두 서비스와 두 개의 volume만 정의 | fastapi/compose.yaml | 폴더 구조보다 실제 compose runtime이 이 프로젝트의 진짜 범위를 더 정확히 말해 준다 | claims-only 흐름을 system test로 고정 |
| 3 | Phase 3, system test가 경계를 최소 증명으로 고정 | identity token만으로 workspace 생성이 가능한지 확인 | tests/test_system.py | 서비스별 unit test만 통과하면 경계 설명이 충분할 것 | identity register/verify/login 후 access token을 workspace-service `/internal/workspaces`에 bearer로 전달하는 시나리오 추가 | `make test` | workspace 생성 요청은 claims가 담긴 bearer token만 사용하고, cross-service DB 조회는 등장하지 않음 | tests/test_system.py::test_identity_token_then_workspace_creation | 서비스 분리의 첫 증거는 복잡한 orchestration보다 '상대 서비스 DB를 읽지 않고도 한 동작이 끝나는가'다 | 실제 재검증 결과 연결 |
| 4 | 2026-03-10 재검증 + 2026-03-11 track polish | 새 MSA 트랙의 출발점이 실제로 다시 실행됐다는 사실 기록 | docs/verification-report.md, fastapi/README.md | 서비스 경계 설명만으로도 이 랩의 목적이 충분할 것 | `make lint`, `make test`, `make smoke` 재실행 결과를 남김 | `make lint`, `make test`, `make smoke` | 2026-03-10 기준 lint, service unit test, system test, smoke 통과 | docs/verification-report.md H-service-boundary-lab 항목 | MSA의 첫 단계에서도 결국 검증은 서비스 unit + system smoke 조합으로 닫힌다 | 비동기 이벤트 통합으로 확장 |
