# 문제 정의

## 문제

동기 API와 비동기 알림 전달을 서비스 간 통합으로 확장한다. 댓글 저장과 알림 생성이 같은 시점에 끝나지 않아도 되는 구조를 설명하는 것이 목표다.

## 성공 기준

- 댓글 생성이 outbox에 기록된다.
- relay 후 `notification-service`가 stream을 consume한다.
- 같은 consume를 두 번 실행해도 알림이 중복 저장되지 않는다.

## 제외 범위

- consumer group
- dead-letter queue
- replay UI
