# 문제 프레이밍

## 학습 목표

I 랩의 목표는 “댓글 저장과 알림 전달은 같은 트랜잭션이 아니다”를 서비스 경계에서 설명하는 것이다. 그래서 `workspace-service`는 outbox까지만 책임지고, `notification-service`는 stream consume와 dedupe만 맡는다.

## 왜 중요한가

- 모놀리식 구조에서는 댓글 저장 직후 같은 프로세스 안에서 알림을 바로 만들기 쉽다.
- 하지만 서비스를 나누면 저장과 전달 사이에 실패 지점이 생기고, 그 사이를 설명하는 장치가 필요하다.
- outbox와 idempotent consumer는 이 간격을 제품 기능이 아니라 시스템 경계로 다루게 해 준다.

## 선수 지식

- H 랩의 claim 기반 service boundary
- Redis 기본 개념과 메시지 전달 흐름
- eventual consistency가 허용하는 지연에 대한 감각

## 성공 기준

- comment 생성이 워크스페이스 데이터와 outbox row를 함께 남겨야 한다.
- relay 후 `notification-service`가 같은 이벤트를 두 번 consume해도 알림은 한 번만 남아야 한다.
- `comment.created.v1`, `invite.accepted.v1` 계약의 의미가 문서와 테스트에 드러나야 한다.

## 일부러 제외한 범위

- consumer group 튜닝과 복잡한 retry 정책
- saga orchestration
- distributed tracing과 운영 대시보드

## 이 랩이 답하려는 질문

- 왜 outbox는 “비동기 기술”이 아니라 “트랜잭션 경계 문서”인가
- relay와 consumer를 분리하면 어떤 실패를 흡수할 수 있는가
- eventual consistency를 허용해도 되는 기능과 안 되는 기능은 어떻게 다를까
