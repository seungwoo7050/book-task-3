# I-event-integration-lab 구조 계획

## 문서 목표

이 랩을 "eventual consistency와 idempotent consumer를 처음 손에 잡히게 만드는 단계"로 읽게 만든다. comment 저장부터 notification 저장까지를 하나의 마법 같은 성공으로 포장하지 않고, outbox, relay, consume을 나눠 설명한다.

## 중심 논지

현재 검증된 핵심은 세 줄이다.

- comment와 outbox는 `workspace-service` 내부 트랜잭션으로 묶인다.
- Redis Stream은 서비스 간 handoff 경계다.
- 중복 읽기 방지는 broker offset이 아니라 `ConsumerReceipt(event_id)`가 맡는다.

## 본문 순서

1. 문제 정의에서 요구한 성공 기준을 먼저 고정한다.
2. compose 런타임이 `workspace-service + notification-service + redis`라는 점을 보여 준다.
3. comment 저장과 outbox 적재를 같은 트랜잭션으로 읽는다.
4. relay가 무엇을 보장하고 무엇을 보장하지 않는지 구분한다.
5. consumer가 `xread("0-0")`와 receipt dedupe로 중복을 흡수한다는 점을 설명한다.
6. system test가 auth를 생략하고 event flow만 검증하는 이유를 연결한다.
7. 실제 재실행 결과를 성공/실패로 나눠 기록한다.

## 반드시 포함할 근거

- `compose.yaml`의 세 서비스 구성
- `create_comment()`의 outbox 적재
- `relay_outbox()`의 Redis `xadd()`와 `relayed` 상태 전이
- `NotificationService.consume()`의 `xread("0-0")` + `has_receipt()` 흐름
- `ConsumerReceipt.event_id` unique 제약
- `tests/test_system.py`의 double consume 검증
- `make lint`, `make test`, `make smoke`, `python3 -m pytest tests/test_system.py -q` 재실행 결과

## 반드시 피할 서술

- notification 저장까지 하나의 원자적 트랜잭션처럼 묘사하지 않는다.
- consumer group이나 offset checkpoint가 이미 구현된 것처럼 쓰지 않는다.
- 인증 흐름이 여전히 이 랩의 주인공인 것처럼 설명하지 않는다.
- 단순히 "Redis를 붙였다" 수준의 얕은 요약으로 끝내지 않는다.

## 품질 체크

- chronology가 살아 있는가
- handoff 경계가 실제 코드 단위로 설명되는가
- dedupe가 어디서 일어나는지 독자가 바로 이해할 수 있는가
- 현재 한계와 제외 범위를 숨기지 않았는가
