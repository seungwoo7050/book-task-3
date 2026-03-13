# K-distributed-ops-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README와 docs가 분산 운영성을 별도 주제로 삼고, `compose.yaml`, `ops.py`, system test, verification report가 service별 health와 request correlation을 함께 다룬다.
- 프로젝트 질문: gateway와 내부 서비스가 동시에 존재할 때, 운영성 surface는 어디서부터 service-local이고 어디서부터 system-level인가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/K-distributed-ops-lab/README.md`
- `labs/K-distributed-ops-lab/problem/README.md`
- `labs/K-distributed-ops-lab/docs/README.md`
- `labs/K-distributed-ops-lab/fastapi/README.md`
- `labs/K-distributed-ops-lab/fastapi/Makefile`
- `labs/K-distributed-ops-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/K-distributed-ops-lab/fastapi/gateway/app/api/v1/routes/ops.py`
- `backend-fastapi/labs/K-distributed-ops-lab/fastapi/tests/test_system.py`
- `git log -- backend-fastapi/labs/K-distributed-ops-lab`

## 프로젝트 표면 요약
- 문제 요약: MSA 구조를 실행만 하는 것으로 끝내지 않고, 서비스별 health, JSON 로그, 최소 metrics, target shape 문서를 함께 설명해야 한다. 이 랩은 운영성을 별도 학습 주제로 분리한다. gateway와 내부 서비스가 각각 `/health/live`, `/health/ready`, `/ops/metrics`를 제공한다. request id가 로그 문맥과 응답 헤더에 남는다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: gateway와 내부 서비스가 각각 `/health/live`, `/health/ready`, `/ops/metrics`를 제공한다. request id가 로그 문맥과 응답 헤더에 남는다. AWS target shape 문서가 실제 배포 완료처럼 쓰이지 않는다.
- 설계 질문: 서비스별 readiness는 무엇을 확인해야 하는가 request id와 metrics는 어떤 운영 질문에 답하는가 target shape 문서는 어디까지 사실이고 어디부터 가정인가 gateway health와 내부 서비스 health를 왜 같은 의미로 보면 안 되는가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-11 89dc218 feat: add new project in fastapi (MSA)

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-11 add project commit 89dc218을 기준으로 복원 | 분산 구조에서 health, logs, metrics를 별도 학습 주제로 분리 | README.md, problem/README.md, docs/README.md | gateway와 services가 돌면 운영성 설명도 자연스럽게 따라올 것 | service별 `/health/live`, `/health/ready`, `/ops/metrics`, request id 로그, AWS target shape를 성공 기준에 포함 | README의 `docker compose up --build` | 문제 정의가 service별 health/metrics와 request id, target shape를 명시 | problem/README.md 성공 기준 | 분산 시스템에서는 기능 surface와 운영 surface를 따로 보지 않으면 설명이 금방 뭉개진다 | gateway와 service-local metrics 구분 |
| 2 | Phase 2, ops route와 compose health를 중심으로 복원 | gateway public health와 내부 service ready를 서로 다른 질문으로 다루기 | gateway/app/api/v1/routes/ops.py, service ops routes, fastapi/compose.yaml | health endpoint 이름만 같으면 의미도 같을 것 | 각 서비스에 live/ready/metrics를 두고, compose healthcheck와 request id 포함 JSON 로그를 결합 | `make test`, `docker compose up --build` | gateway metrics가 `app_requests_total{service="gateway"}`처럼 service label을 포함 | gateway/app/api/v1/routes/ops.py::metrics | 분산 운영성에서 같은 `/health/ready`라도 서비스마다 다른 질문에 답할 수 있다 | system flow와 장애 회복으로 운영 surface 검증 |
| 3 | Phase 3, system test와 compose harness가 분산 운영성을 고정 | notification-service 장애 전후 comment 흐름과 recovery를 확인 | tests/test_system.py, tests/compose_harness.py | metrics와 health만 확인하면 운영성 글도 충분할 것 | notification-service stop/start 사이에 comment 생성, failed drain 503, recovery drain 성공, websocket 재수신 시나리오 유지 | `make test`, `make smoke` | notification-service 중단 중 drain 503, 복구 뒤 websocket으로 second comment 알림 도착 | tests/test_system.py::test_v2_system_flow_and_notification_recovery | 운영성 글은 steady-state보다 장애 중 어떤 API가 실패하고 어떤 API는 계속 성공하는지 보여 줘야 한다 | 재검증 보고서와 연결 |
| 4 | 2026-03-10 재검증 + 2026-03-11 track polish | 분산 운영성 랩의 실제 재실행 사실 남기기 | docs/verification-report.md, fastapi/README.md | ops 랩은 문서만 잘 써도 충분할 것 | `make test`, `make smoke` 재실행 결과를 남기고 gateway/identity/workspace/notification unit + system + smoke 통과 기록 | `make test`, `make smoke`, `docker compose up --build` | 2026-03-10 기준 gateway/identity/workspace/notification unit test, system test, smoke 통과 | docs/verification-report.md K-distributed-ops-lab 항목 | 분산 운영성도 결국 실행 기록이 있어야 문서가 target shape를 넘는다 | MSA capstone v2와 비교 |
