# workspace-backend-v2-msa Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: capstone README, docs, compose, system test, verification report가 gateway + services 구조와 notification-service 장애 복구까지 독립적으로 설명한다.
- 프로젝트 질문: v1과 같은 협업형 도메인을 MSA로 다시 풀었을 때 무엇이 단순해지고 무엇이 더 복잡해지는가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `capstone/workspace-backend-v2-msa/README.md`
- `capstone/workspace-backend-v2-msa/problem/README.md`
- `capstone/workspace-backend-v2-msa/docs/README.md`
- `capstone/workspace-backend-v2-msa/fastapi/README.md`
- `capstone/workspace-backend-v2-msa/fastapi/Makefile`
- `capstone/workspace-backend-v2-msa/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/compose.yaml`
- `backend-fastapi/capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py`
- `git log -- backend-fastapi/capstone/workspace-backend-v2-msa`

## 프로젝트 표면 요약
- 문제 요약: `workspace-backend` v1은 인증, 워크스페이스 도메인, 알림 전달을 한 프로세스 안에서 통합했다. v2의 목표는 같은 협업형 도메인을 MSA로 다시 분해해, public API를 유지한 채 내부 경계와 분산 복잡성이 어떻게 바뀌는지 설명 가능한 상태로 만드는 것이다. `gateway`가 public `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지해야 한다. `identity-service`, `workspace-service`, `notification-service`는 각자 자기 DB만 읽어야 한다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: `gateway`가 public `/api/v1/auth/*`, `/api/v1/platform/*` 경로를 유지해야 한다. `identity-service`, `workspace-service`, `notification-service`는 각자 자기 DB만 읽어야 한다. 댓글 생성은 outbox에 기록되고, 이후 stream consumer와 websocket fan-out으로 이어져야 한다. notification-service가 잠시 내려가도 댓글 생성은 성공하고, 복구 후 consume로 알림이 전달되어야 한다. v1과 v2의 차이를 문서와 노트만 읽고 설명할 수 있어야 한다.
- 설계 질문: 왜 `platform`을 그대로 두지 않고 `identity/workspace/notification`으로 나눴는가 public API는 왜 gateway에서 유지하는가 outbox, stream, pub/sub은 각각 어느 경계에 필요한가 v1보다 좋아진 점과 나빠진 점은 무엇인가 무엇이 실제 검증된 사실이고, 무엇이 아직 target shape 문서 수준의 가정인가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-11 a6026ef 기본 과정 필수 / 심화 섹션 분류
- 2026-03-11 89dc218 feat: add new project in fastapi (MSA)

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-11 add project commit 89dc218 + a6026ef를 기준으로 복원 | v1의 협업 도메인을 MSA 구조로 다시 풀기 | README.md, problem/README.md, docs/README.md | 서비스를 쪼개면 자동으로 구조가 더 좋아질 것 | gateway가 public API shape를 유지하고, identity/workspace/notification이 각자 DB를 소유하도록 재정의 | README의 `docker compose up --build`, `make test` | README가 v1과의 비교, DB ownership, eventual consistency를 한 답으로 설명 | README.md / docs/README.md 비교 질문 | MSA capstone의 핵심은 서비스 수가 아니라 v1보다 무엇이 복잡해졌는지 설명 가능해지는 데 있다 | runtime scope와 public path 고정 |
| 2 | Phase 2, compose/runtime scope를 중심으로 복원 | gateway + identity + workspace + notification + redis를 실제 비교 대상 runtime으로 고정 | fastapi/compose.yaml, fastapi/README.md, gateway/app/api/v1/routes/platform.py | 문서만 있으면 MSA 경계가 충분히 전달될 것 | compose에 다섯 서비스와 healthcheck를 두고, gateway가 public `/api/v1/auth/*`, `/api/v1/platform/*`를 유지 | `docker compose up --build` | compose가 8015/8115/8116/8117/6395 포트의 runtime을 정의 | fastapi/compose.yaml | 비교 가능한 MSA는 먼저 실제 runtime surface가 분명해야 한다 | public flow와 장애 복구를 system test로 증명 |
| 3 | Phase 3, system test가 v2의 차이를 드러냄 | owner local auth, collaborator Google login, invite, comment, notification failure/recovery, websocket fan-out을 한 번에 검증 | tests/test_system.py | 서비스별 unit test를 합치면 capstone 설명도 끝날 것 | public `/api/v1/*`만 호출해 협업 흐름을 수행하고, notification-service stop/start 사이의 drain 503과 recovery drain 성공까지 테스트화 | `python -m pytest tests/test_system.py -q`에 해당하는 흐름, `make test` | 첫 drain 성공 뒤 websocket 수신, notification-service 중단 중 drain 503, 복구 뒤 두 번째 알림 수신 | tests/test_system.py::test_v2_system_flow_and_notification_recovery | v2의 핵심 차이는 기능 수가 아니라, 성공 경로와 장애 경로가 다른 서비스에서 끝난다는 사실이다 | 실제 재검증과 Docker 이슈를 사실대로 기록 |
| 4 | 2026-03-10 재검증 + 2026-03-11 track polish | v2의 실제 검증 범위와 아직 불안정한 fresh build 경로를 분리해서 기록 | docs/verification-report.md, fastapi/README.md | Compose runtime이 한 번 올라오면 fresh build도 성공한 것처럼 적어도 괜찮을 것 | service unit tests는 통과로 기록하고, fresh build 실패 징후와 Docker Desktop 재시작 후 prebuilt image 기준 end-to-end 재검증 사실을 분리해 적음 | `make test`, `docker compose up --build -d` 재시도, `docker build ...`, `docker pull python:3.12-slim`, 복구 후 `docker compose ... up -d --no-build` | fresh build 성공은 기록하지 않음. 대신 prebuilt image 기준 Compose runtime + end-to-end 협업 흐름 검증 완료 | docs/verification-report.md workspace-backend-v2-msa 항목 | 분산 capstone에서는 실패한 검증 경로까지 사실대로 분리해 적는 태도가 특히 중요하다 | v1과의 비교 정리 |
