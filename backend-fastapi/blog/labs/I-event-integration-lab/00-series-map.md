# I-event-integration-lab

이 글은 저장과 알림 생성을 같은 트랜잭션으로 두지 않을 때 무엇을 먼저 증명해야 하는지를 따라간다. I 랩은 comment를 썼다는 사실과 notification이 나중에 전달된다는 사실을 분리해, eventual consistency를 실제 흐름으로 읽게 만든다.

## 이 글이 붙잡는 질문
comment 저장과 notification 생성을 이벤트로 끊어 두었을 때, 유실 없이 다시 처리되고 중복 없이 소모된다는 점을 어떤 근거로 설명할 수 있는가가 이 글의 핵심 질문이다.

## 왜 이 프로젝트를 따로 읽어야 하나
README와 docs가 relay, consumer, dedupe를 별도 경계로 설명하고, compose와 system test는 workspace-service, notification-service, redis만으로 그 흐름을 재현한다. 그래서 이 프로젝트는 이벤트 통합의 가장 작은 독립 사례가 된다.

## 이번 글에서 따라갈 흐름
1. 저장과 알림 생성을 eventual consistency 문제로 다시 본다.
2. runtime을 workspace, notification, redis 셋으로 제한한다.
3. relay와 두 번 consume, dedupe를 system test로 고정한다.
4. 재검증 기록으로 이벤트 통합 경계를 닫는다.

## 마지막에 확인할 근거
- 코드: `labs/I-event-integration-lab/fastapi/compose.yaml::__compose__`
- 테스트/런타임: `labs/I-event-integration-lab/fastapi/tests/test_system.py::test_outbox_and_idempotent_consumer_flow`
- CLI: `make lint`, `make test`, `make smoke`, `docker compose up --build`

## 이 글을 다 읽고 나면
- event relay와 consumer가 왜 다른 책임을 갖는지 이해하게 된다.
- 중복 소비와 dedupe가 결국 같은 장애 복구 문제라는 점이 보인다.
- 동기 성공 응답과 비동기 완료를 어떻게 분리해서 써야 하는지 감이 잡힌다.
- 검증 기록: 2026-03-10에 lint, service unit test, system test, smoke가 통과했다.
- 다음으로 이어 볼 대상: J-edge-gateway-lab
