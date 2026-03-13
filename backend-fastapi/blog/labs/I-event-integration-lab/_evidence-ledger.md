# I-event-integration-lab Evidence Ledger

## 독립 프로젝트 판정
- 판정: 처리 대상
- 이유: README와 docs가 outbox, Redis Streams relay, dedupe를 핵심으로 설명하고, `compose.yaml`과 `tests/test_system.py`가 workspace-service와 notification-service의 실제 경계와 중복 consume 흡수를 재현한다.
- 프로젝트 질문: 댓글 저장과 알림 생성을 같은 순간에 끝내지 않아도 된다고 말하려면, 어떤 전달 경로와 중복 흡수 장치를 보여줘야 하는가.
- 주의: finer-grained 구현 순서는 commit granularity가 거칠어서 README, docs, code surface, tests 의존 순서를 바탕으로 복원했다. 실제 날짜가 확인되는 부분은 git log와 검증 보고서에만 한정했다.

## 소스 인벤토리
- `labs/I-event-integration-lab/README.md`
- `labs/I-event-integration-lab/problem/README.md`
- `labs/I-event-integration-lab/docs/README.md`
- `labs/I-event-integration-lab/fastapi/README.md`
- `labs/I-event-integration-lab/fastapi/Makefile`
- `labs/I-event-integration-lab/fastapi/compose.yaml`
- `backend-fastapi/.github/workflows/labs-fastapi.yml`
- `backend-fastapi/docs/verification-report.md`
- `backend-fastapi/labs/I-event-integration-lab/fastapi/compose.yaml`
- `backend-fastapi/labs/I-event-integration-lab/fastapi/tests/test_system.py`
- `git log -- backend-fastapi/labs/I-event-integration-lab`

## 프로젝트 표면 요약
- 문제 요약: 동기 API와 비동기 알림 전달을 서비스 간 통합으로 확장한다. 댓글 저장과 알림 생성이 같은 시점에 끝나지 않아도 되는 구조를 설명하는 것이 목표다. 댓글 생성이 outbox에 기록된다. relay 후 `notification-service`가 stream을 consume한다. 상세 성공 기준과 제외 범위는 problem/README.md에 둡니다.
- 성공 기준: 댓글 생성이 outbox에 기록된다. relay 후 `notification-service`가 stream을 consume한다. 같은 consume를 두 번 실행해도 알림이 중복 저장되지 않는다.
- 설계 질문: outbox가 왜 여전히 필요한가 stream payload에는 무엇을 넣고 무엇을 넣지 않는가 idempotent consumer는 어떤 실패를 흡수하는가 relay와 consumer를 같은 서비스에 두지 않는 이유는 무엇인가
- 실제 검증 surface: make lint make test make smoke docker compose up --build 실행과 환경 설명은 fastapi/README.md에서 다룹니다. 마지막 기록된 실제 검증 결과는 ../../docs/verification-report.md에 있습니다.

## 시간 표지
- 2026-03-11 bbb6673 Track 1에 대한 전반적인 개선 완료
- 2026-03-11 89dc218 feat: add new project in fastapi (MSA)

## Chronology Ledger
| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1, 2026-03-11 add project commit 89dc218을 기준으로 복원 | 댓글 저장과 알림 생성을 같은 트랜잭션으로 묶지 않는 구조 정리 | README.md, problem/README.md, docs/README.md | notification-service만 추가하면 서비스 통합 설명이 될 것 | outbox 적재, relay, consume, dedupe를 핵심 성공 기준으로 설정 | README의 `docker compose up --build` | 문제 정의가 outbox 기록, relay, idempotent consume를 직접 요구 | problem/README.md 성공 기준 | 서비스 통합의 핵심은 호출 수가 아니라 데이터가 어느 시점에 확정되는지다 | runtime scope를 event path 중심으로 고정 |
| 2 | Phase 2, compose/runtime scope를 중심으로 복원 | workspace와 notification을 Redis Streams로만 연결되는 구조 만들기 | fastapi/compose.yaml, fastapi/README.md | identity나 gateway도 함께 있어야 이벤트 통합을 설명할 수 있을 것 | compose에는 workspace-service, notification-service, redis만 올리고 relay/consumer path에 집중 | `docker compose up --build` | compose.yaml이 workspace-service, notification-service, redis만 정의 | fastapi/compose.yaml | 이벤트 통합은 전체 MSA가 아니라 producer와 consumer만 있어도 충분히 설명할 수 있다 | relay와 dedupe를 system test로 고정 |
| 3 | Phase 3, system test가 eventual consistency를 증명 | comment 생성 뒤 outbox pending, relay, 두 번 consume, notification 1건 저장을 검증 | tests/test_system.py | producer와 consumer 각각의 unit test면 충분할 것 | comment 작성 뒤 pending outbox 1건 확인, relay 후 첫 consume=1, 두 번째 consume=0, collaborator notification 1건 저장 확인 | `make test` | 두 번 consume해도 두 번째 processed 값이 0 | tests/test_system.py::test_outbox_and_idempotent_consumer_flow | eventual consistency를 설명할 때 가장 중요한 숫자는 지연 시간이 아니라 중복 소비 후 남는 결과 수다 | 실제 재검증 결과 연결 |
| 4 | 2026-03-10 재검증 + 2026-03-11 track polish | 새 이벤트 통합 랩이 실제로 다시 실행됐다는 사실 확인 | docs/verification-report.md, fastapi/README.md | 이벤트 계약 설명만 있으면 충분할 것 | `make lint`, `make test`, `make smoke` 재실행 결과를 남김 | `make lint`, `make test`, `make smoke` | 2026-03-10 기준 lint, service unit test, system test, smoke 통과 | docs/verification-report.md I-event-integration-lab 항목 | eventual consistency도 마지막엔 단순 CLI로 재현 가능한 시나리오로 닫혀야 한다 | edge gateway 도입으로 public API shape 유지 |
