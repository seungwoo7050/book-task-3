# I-event-integration-lab 시리즈 맵

H 랩이 "서비스를 어디서 끊을까"를 다뤘다면, 이 랩은 "끊어진 뒤에 동기 흐름과 비동기 알림을 어떻게 다시 이어 붙일까"를 다룬다. 중심은 `workspace-service`의 outbox, Redis Streams relay, `notification-service`의 idempotent consumer다. 중요한 점은 댓글 저장과 알림 생성이 같은 순간에 끝나지 않아도 된다는 사실을 코드와 검증으로 설명하는 것이다.

## 이 랩에서 끝까지 붙잡은 질문

- comment 저장과 notification 저장을 왜 같은 트랜잭션으로 묶지 않는가
- outbox는 어디까지 책임지고, relay는 어디서 handoff를 끝내는가
- consumer group 없이도 중복 consume를 어떻게 흡수하는가
- 이 랩에서 auth 서비스가 빠진 이유는 무엇인가

## 이 문서 묶음이 내린 현재 결론

- 현재 검증된 런타임은 `workspace-service + notification-service + redis` 조합이다.
- `workspace-service`는 comment와 outbox event를 같은 서비스 DB 트랜잭션 안에서 커밋한다.
- `relay_outbox()`는 pending outbox를 Redis Stream으로 밀어 넣고 `relayed`로 표시한다.
- `notification-service`는 stream을 매번 처음부터 읽어도 `ConsumerReceipt(event_id)`로 중복 저장을 막는다.
- 다만 `consume()` 한 번이 stream 전체를 무한히 비우는 것은 아니다. 현재 구현은 `xread(..., count=100)` 한 배치만 읽고, system test도 1건 흐름을 기준으로 이 경계를 검증한다.
- system test가 JWT를 직접 서명하는 이유는, 이 랩의 초점이 인증이 아니라 event handoff와 idempotency이기 때문이다.

## 추천 읽기 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-plan.md`

## 각 문서의 역할

- `10-development-timeline.md`: outbox 생성, relay handoff, consumer dedupe, 검증 결과를 시간순으로 정리한다.
- `_evidence-ledger.md`: 관련 소스, 테스트, 명령 재실행 결과를 근거 중심으로 정리한다.
- `_structure-plan.md`: 이 랩을 eventual consistency 입문 문서로 읽기 위한 설명 순서를 남긴다.

## 이번에 다시 확인한 검증 스냅샷

- `make lint`: 통과
- `make test`: 로컬 `python3` 환경에서 `workspace-service` 테스트 collection 중 `ModuleNotFoundError: No module named 'argon2'`
- `make smoke`: 통과
- `python3 -m pytest tests/test_system.py -q`: 통과

이 랩의 핵심은 "한 번만 전달"이 아니라 "여러 번 읽어도 결과는 한 번만 남긴다"는 쪽에 더 가깝다. 그 차이를 놓치지 않는 것이 시리즈 전체를 읽는 포인트다.
