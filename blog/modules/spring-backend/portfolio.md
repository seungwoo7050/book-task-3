# Spring Backend Portfolio Module

| 항목 | 내용 |
| --- | --- |
| 포지셔닝 | modular monolith, JPA/Flyway, Redis, outbox/Kafka, Testcontainers를 갖춘 Spring 포트폴리오 백엔드 |
| 대표 프로젝트 | `commerce-backend-v2`, `B-federation-security-lab`, `E-event-messaging-lab` |
| 핵심 스택 | Spring Boot, JPA, Flyway, Redis, Kafka, Testcontainers, MockMvc |

## 메인 프로젝트

### commerce-backend-v2

같은 커머스 도메인을 baseline보다 더 깊게 구현한 portfolio-grade capstone입니다. persisted auth, JPA + Flyway domain modeling, Redis cart/throttling, idempotent payment, outbox + Kafka notification을 modular monolith 구조로 묶었습니다.

### 보조 근거

- `B-federation-security-lab`: OAuth2 federation, 2FA, audit 강화
- `E-event-messaging-lab`: outbox와 messaging 경계 기초

## 메인 캡처

![commerce backend v2 evidence](../../assets/captures/spring-backend/commerce-backend-v2-evidence.png)

## 마무리

이 모듈은 Spring 백엔드를 기술 키워드 집합이 아니라, 같은 도메인을 baseline에서 portfolio-grade로 끌어올린 결과물로 보여 줍니다. 인증, 데이터, 이벤트, 운영성, 검증을 함께 설명할 수 있다는 점이 핵심입니다.
