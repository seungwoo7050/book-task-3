# notification-service

- 범위: Redis Streams consumer, idempotent receipt, 알림 저장, gateway pub/sub 발행
- 실행: `make install && make run`
- 테스트: `make test`
- 상태: 학습용 구현 완료
- 비고: `workspace-service` DB를 읽지 않고 stream payload만 소비합니다.
