# commerce-backend-v2 문제 정의

Spring 랩들의 학습을 하나의 커머스 도메인으로 다시 조합하되, junior backend interview에서 방어 가능한 깊이까지 끌어올린 대표 capstone을 만든다.

## 성공 기준

- persisted local auth와 mocked Google account linking이 존재한다.
- JPA + Flyway + PostgreSQL로 catalog, order, payment, notification 경계를 설명할 수 있다.
- Redis와 Kafka가 cart, throttling, outbox handoff 같은 구체적 문제에 연결된다.
- Docker Compose, health/readiness, metrics, 테스트, 배포 메모가 함께 남는다.

## 이번 단계에서 다루지 않는 것

- live Google OAuth console integration
- 실제 payment provider integration
- live AWS provisioning과 장기 운영 검증

이 디렉터리는 대표 capstone의 canonical problem statement와 성공 기준을 담당한다.
