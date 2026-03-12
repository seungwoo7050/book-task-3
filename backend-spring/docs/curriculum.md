# backend-spring 커리큘럼

이 레포는 FastAPI 트랙의 단순 번역이 아니라, Spring Boot 백엔드에서 자주 요구되는 문제를 독립 랩으로 나눈 뒤 커머스 캡스톤으로 다시 조합하는 학습 프로그램입니다.

## 순서

1. `A-auth-lab`: 로컬 인증, refresh rotation, 이메일 검증, 비밀번호 재설정
2. `B-federation-security-lab`: Google OAuth2 callback 모델링, 2FA, audit, throttling
3. `C-authorization-lab`: membership, RBAC, ownership, invite flow
4. `D-data-jpa-lab`: JPA 매핑, Flyway, pagination, optimistic locking, Querydsl-ready structure
5. `E-event-messaging-lab`: outbox pattern, Kafka handoff, retry와 DLQ 사고방식
6. `F-cache-concurrency-lab`: 캐시, 멱등성, 재고 경합, 분산 락으로 이어지는 문제의식
7. `G-ops-observability-lab`: health, metrics, logs, CI, 배포 메모
8. `capstone/commerce-backend`: 7개 랩의 학습을 한 도메인으로 다시 조합한 baseline
9. `capstone/commerce-backend-v2`: 같은 도메인을 더 깊게 구현한 대표 결과물

## 이 순서가 가르치는 것

- 인증과 인가를 먼저 분리해 "누구인가"와 "무엇을 할 수 있는가"를 섞지 않게 합니다.
- 데이터/JPA 문제를 별도 랩으로 떼어 프레임워크 사용과 데이터 경계 설계를 함께 보게 합니다.
- 이벤트, 캐시, 운영성은 기능 부록이 아니라 서비스 신뢰성 문제로 연결합니다.
- 캡스톤에서는 랩 코드를 재사용하지 않고 같은 개념을 다시 구현해, 최종 결과물이 하나의 일관된 서비스로 읽히게 합니다.

## 취업 관점에서 강조하는 신호

- Spring Security 기반 인증 흐름
- JPA, Flyway, PostgreSQL 중심 persistence
- Redis와 Kafka를 "보여주기용"이 아니라 특정 문제 해결 수단으로 쓰는 판단
- idempotency, optimistic locking, health/readiness, structured logging 같은 운영 기본기

## 캡스톤 위계

- [commerce-backend](../capstone/commerce-backend/README.md)는 baseline입니다.
- [commerce-backend-v2](../capstone/commerce-backend-v2/README.md)는 이 레포에서 가장 강한 대표 결과물입니다.
- 두 캡스톤을 함께 두는 이유는 기능 수 경쟁이 아니라, baseline 대비 무엇을 더 깊게 구현했는지 설명하기 위해서입니다.
