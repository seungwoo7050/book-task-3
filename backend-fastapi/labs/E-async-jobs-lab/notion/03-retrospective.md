# 회고

## 이번 랩에서 얻은 것

비동기 작업은 "Celery를 쓴다"보다 "어디서 안전하게 넘길 것인가"가 더 중요하다는 점이 선명해졌다. outbox와 idempotency를 함께 설명할 수 있게 된 것이 가장 큰 수확이다.

## 아직 약한 부분

- 운영용 재처리 도구나 dead-letter 흐름은 없다.
- 실제 분산 환경에서의 drain 동시성은 문서 수준으로만 남아 있다.

## 다시 보면 좋을 주제

- advisory lock / SELECT FOR UPDATE
- dead-letter queue
- 작업 모니터링 화면

## 포트폴리오 확장 아이디어

- 작업 재실행 API와 실패 알림 채널을 추가한다.
- Kafka, SQS 같은 대안을 비교하는 실험 랩을 별도로 만든다.
