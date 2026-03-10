# 접근 로그

## 처음 고려한 선택지

1. comment 저장 시 notification-service HTTP API를 동기 호출한다.
2. comment 저장 후 같은 서비스 내부 worker가 알림까지 만든다.
3. comment 저장은 outbox까지만 책임지고, relay + stream + idempotent consumer로 후속 처리를 넘긴다.

## 선택한 방향

세 번째 방식을 택했다. 저장 경계와 전달 경계를 일부러 분리하고, 중복 소비는 receipt 기반 dedupe로 흡수한다.

## 그렇게 고른 이유

- 동기 HTTP 호출은 notification-service 장애가 comment 저장 자체를 실패시키기 쉽다.
- 내부 worker 방식은 서비스 경계를 설명하기 어렵고, I 랩의 학습 목표가 흐려진다.
- outbox + consumer 방식은 불편하지만 “저장 성공”과 “전달 성공”을 다른 사건으로 분리해 설명할 수 있다.

## 의도적으로 단순화한 점

- Redis Streams를 단순 consume로 사용하고 복잡한 consumer group 운영은 다루지 않는다.
- retry queue나 dead letter queue를 추가하지 않는다.
- 이벤트 계약도 `comment.created.v1`, `invite.accepted.v1` 두 종류로 제한한다.

## 이번 선택이 만든 제약

- 알림 전달은 즉시성이 아니라 eventual consistency를 전제로 한다.
- consumer는 idempotency를 위해 receipt 테이블을 유지해야 한다.
- relay 실패와 consume 실패를 따로 관찰해야 한다.
