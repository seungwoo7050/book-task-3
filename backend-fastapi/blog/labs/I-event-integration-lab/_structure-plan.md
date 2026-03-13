# I-event-integration-lab Structure Plan

## 한 줄 약속
- 동기 API 뒤에 outbox와 idempotent consumer를 붙여 eventual consistency를 드러내기

## 독자 질문
- 댓글 저장과 알림 생성을 같은 순간에 끝내지 않아도 된다고 말하려면, 어떤 전달 경로와 중복 흡수 장치를 보여줘야 하는가.
- outbox가 왜 여전히 필요한가 stream payload에는 무엇을 넣고 무엇을 넣지 않는가 idempotent consumer는 어떤 실패를 흡수하는가 relay와 consumer를 같은 서비스에 두지 않는 이유는 무엇인가

## 서술 원칙
- 기존 `blog/` 초안은 입력 근거로 사용하지 않는다.
- 사실로 확인되는 날짜와 명령은 `git log`와 `docs/verification-report.md`에서만 가져온다.
- finer-grained chronology는 코드/테스트 의존 순서를 바탕으로 복원했다고 명시한다.

## 글 흐름
1. 서비스 통합을 동기 API 대신 이벤트 전달 문제로 보기
2. compose runtime을 workspace + notification + redis로 좁히기
3. system test로 relay와 dedupe를 고정하기
4. 2026-03-10 재검증으로 eventual consistency surface를 닫기
5. 남은 범위와 다음 비교 대상 정리

## Evidence Anchor
- 주 코드 앵커: `labs/I-event-integration-lab/fastapi/compose.yaml::__compose__` — runtime이 workspace-service, notification-service, redis 셋으로 닫혀 있음을 보여 준다.
- 보조 앵커: `labs/I-event-integration-lab/fastapi/tests/test_system.py::test_outbox_and_idempotent_consumer_flow` — comment 저장, relay, 두 번 consume, notification dedupe를 한 흐름으로 고정한다.
- 문서 앵커: `labs/I-event-integration-lab/problem/README.md`, `labs/I-event-integration-lab/docs/README.md`
- CLI 앵커:
- `make lint`
- `make test`
- `make smoke`
- `docker compose up --build`

## 글에서 강조할 개념
- `comment.created.v1` 계약 relay와 consume의 책임 차이 eventual consistency가 허용하는 지연 중복 읽기가 있어도 결과를 한 번만 남기는 구조
- outbox handoff를 서비스 경계로 옮기는 방법 Redis Streams 기반 이벤트 전달 idempotent consumer와 중복 흡수 consumer group 대신 단순 consumer 흐름으로 제한합니다. dead-letter queue와 재처리 UI는 범위 밖입니다.

## 끝맺음
- 제외 범위: consumer group dead-letter queue replay UI
- 검증 문장: 2026-03-10에 lint, service unit test, system test, smoke가 통과했다.
