# Approach Log

## Options considered

### Option 1. 기존 `commerce-backend`를 직접 수정한다

- what would have been simpler:
  - 복사 없이 한 경로에서 바로 진화시킬 수 있다.
  - 중복 문서가 생기지 않는다.
- what would have become harder:
  - baseline과 upgraded version의 차이를 설명하기 어려워진다.
  - “학습 이력 보존”이라는 요구를 만족하지 못한다.
- why it stayed viable or was ruled out:
  - 구현 자체는 가능했지만, 이번 과제의 핵심 제약이 N과 N+1을 모두 유지하는 것이었기 때문에 제외했다.

### Option 2. 새로운 도메인으로 갈아탄다

- what would have been simpler:
  - 기존 스캐폴드의 제약에서 덜 묶일 수 있다.
  - 예를 들어 협업 SaaS나 티켓 시스템처럼 더 익숙한 도메인으로 바꿀 수 있다.
- what would have become harder:
  - “기존 캡스톤을 복사해 개선한다”는 과제 의미가 약해진다.
  - 이전 캡스톤과 비교하면서 개선 포인트를 설명하기 어렵다.
- why it stayed viable or was ruled out:
  - 도메인을 유지하고 구현 깊이만 올리는 편이 더 정직한 개선이라고 판단해서 제외했다.

### Option 3. 마이크로서비스 구조로 쪼갠다

- what would have been simpler:
  - Redis, Kafka, auth, catalog를 각각 독립 서비스로 보여주기 쉽다.
  - 인프라 키워드를 많이 넣을 수 있다.
- what would have become harder:
  - 주니어 포트폴리오로서 코드 가독성과 설명 가능성이 크게 떨어진다.
  - 서비스 경계보다 배포 복잡성이 더 큰 이슈가 된다.
- why it stayed viable or was ruled out:
  - 이번 캡스톤의 목적은 서비스 choreography가 아니라 트랜잭션 경계와 백엔드 판단력을 보여주는 것이므로 제외했다.

### Option 4. 모듈형 모놀리스로 유지하되 persisted flow를 끝까지 연결한다

- what would have been simpler:
  - 코드 탐색과 인터뷰 설명이 쉬워진다.
  - Compose와 Testcontainers로 검증하기 좋다.
- what would have become harder:
  - Redis/Kafka를 “보여주기용”이 아니라 실제 기능 흐름에 의미 있게 연결해야 한다.
- why it stayed viable or was ruled out:
  - 최종 선택이다. 기술 선택보다 경계 설정과 데이터 흐름 설명에 유리했다.

## Chosen direction

- package structure:
  - `auth`, `catalog`, `cart`, `order`, `payment`, `notification`, `global`
- persistence choice:
  - 핵심 진실은 PostgreSQL 스키마에 둔다.
  - 로컬 빠른 테스트는 H2로 유지한다.
  - cart와 auth throttling만 Redis로 분리한다.
- security boundary:
  - access token은 stateless Bearer JWT
  - refresh token은 DB-hashed + HttpOnly cookie
  - refresh/logout은 CSRF header 필요
  - admin surface는 `/api/v1/admin/**`로 분리
- integration style:
  - 동기 핵심 플로우는 HTTP + JPA transaction
  - 비동기 처리는 outbox table → publisher → Kafka consumer 한 줄기로 제한
- why this is the right choice for this lab:
  - Spring 취업 시장에서 자주 묻는 JPA, Redis, JWT, Docker, Kafka를 억지 없이 한 프로젝트에 담을 수 있다.
  - 구현의 깊이와 설명 가능성 사이 균형이 가장 좋다.

## Rejected ideas

- refresh token을 서버 저장 없이 self-contained JWT로만 두는 방식은 폐기했다. 회전, 폐기, 재사용 감지를 설명하기 어렵기 때문이다.
- payment 시점에만 재고를 차감하는 방식은 폐기했다. 결제 지연 동안 oversell 위험을 정직하게 다루지 못하기 때문이다.
- Kafka publish를 payment 요청 트랜잭션 안에서 직접 호출하는 방식은 폐기했다. DB와 메시지 브로커 사이의 원자성 설명이 약해지기 때문이다.
- Redis를 product/order read model까지 넓히는 방식은 폐기했다. 포트폴리오 범위 대비 캐시 무효화 설명 비용이 커졌기 때문이다.

## Evidence

- Which code files reflect the decision?
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/src/main/java/com/webpong/study2/app/order/application/OrderService.java`
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/src/main/java/com/webpong/study2/app/payment/application/PaymentService.java`
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/src/main/java/com/webpong/study2/app/cart/infrastructure/RedisCartStore.java`
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/src/main/java/com/webpong/study2/app/notification/infrastructure/OutboxPublisher.java`
  - `/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/src/main/resources/db/migration/V2__commerce.sql`
- Which test or manual verification proved the choice was workable?
  - `CommercePortfolioApiTest`
  - `CommerceMessagingIntegrationTest`
  - `./tools/compose_probe.sh study2/capstone/commerce-backend-v2/spring 8111`
