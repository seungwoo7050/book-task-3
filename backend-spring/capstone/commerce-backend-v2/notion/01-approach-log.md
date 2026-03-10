# Approach Log — 네 가지 선택지에서 모듈형 모놀리스를 고른 이유

## 네 가지 선택지

캡스톤 v2를 시작할 때 고려한 길은 네 가지였다.

**첫 번째: 기존 commerce-backend를 직접 수정한다.** 복사 없이 한 경로에서 바로 진화시킬 수 있고 중복 문서도 발생하지 않는다. 하지만 이 과제의 핵심 제약이 "N과 N+1을 모두 유지한다"였기 때문에 baseline과 upgraded version의 차이를 설명하는 것이 불가능해진다. 학습 이력 보존이라는 요구를 만족하지 못하므로 제외했다.

**두 번째: 새로운 도메인으로 갈아탄다.** 예를 들어 협업 SaaS나 티켓 시스템처럼 더 익숙한 도메인을 선택하면 기존 스캐폴드의 제약에서 벗어날 수 있다. 그러나 "기존 캡스톤을 복사해 개선한다"는 과제 의미가 약해지고, 이전 캡스톤과 비교하면서 개선 포인트를 설명하기 어려워진다. 도메인을 유지하고 구현 깊이만 올리는 편이 더 정직한 개선이라 판단하여 제외했다.

**세 번째: 마이크로서비스 구조로 쪼갠다.** Redis, Kafka, auth, catalog를 각각 독립 서비스로 보여줄 수 있고 인프라 키워드를 많이 넣을 수 있다. 하지만 주니어 포트폴리오에서 코드 가독성과 설명 가능성이 크게 떨어지고, 서비스 경계보다 배포 복잡성이 더 큰 이슈가 된다. 이 캡스톤의 목적은 서비스 choreography가 아니라 트랜잭션 경계와 백엔드 판단력을 보여주는 것이므로 제외했다.

**네 번째: 모듈형 모놀리스로 유지하되 persisted flow를 끝까지 연결한다.** 코드 탐색과 인터뷰 설명이 쉽고, Compose/Testcontainers로 검증하기 좋다. Redis와 Kafka를 "보여주기용"이 아니라 실제 기능 흐름에 의미 있게 연결해야 하는 부담이 있지만, 기술 선택보다 경계 설정과 데이터 흐름 설명에 가장 유리했다. **이 방향을 선택했다.**

## 선택한 구조

최종 구조는 일곱 개 패키지 — `auth`, `catalog`, `cart`, `order`, `payment`, `notification`, `global` — 로 나뉜다.

**데이터 저장소 전략**: 핵심 진실(source of truth)은 PostgreSQL 스키마에 둔다. 로컬 빠른 테스트는 H2로 유지한다. Redis는 cart(장바구니 상태)와 auth throttling에만 사용하여, "모든 곳에 Redis를 넣는" 과시를 피했다.

**보안 경계**: access token은 stateless Bearer JWT로 전달하고, refresh token은 DB에 hash만 저장한 뒤 HttpOnly cookie로 전달한다. refresh와 logout 요청에는 CSRF header를 강제하여, 쿠키 탈취만으로는 갱신할 수 없게 만들었다. admin surface는 `/api/v1/admin/**`로 격리하여 역할 기반 접근을 적용했다.

**통합 방식**: 동기 핵심 흐름(회원가입, checkout, 결제 확인)은 HTTP + JPA transaction으로 처리한다. 비동기 처리는 outbox table → publisher → Kafka consumer 한 줄기로 제한하여, 메시징 레이어가 과도하게 복잡해지는 것을 막았다.

이 구조의 핵심 가치는 Spring 취업 시장에서 자주 묻는 JPA, Redis, JWT, Docker, Kafka를 억지 없이 한 프로젝트에 담되, 구현 깊이와 설명 가능성 사이의 균형을 유지하는 것이다.

## 버린 아이디어들

네 가지 아이디어를 구체적으로 검토한 뒤 버렸다.

**refresh token을 서버 저장 없이 self-contained JWT로만 두는 방식.** 폐기 이유: 토큰 회전, 폐기, 재사용 감지를 면접에서 설명하기 어렵다. DB에 hash를 저장하면 "이 토큰은 아직 유효한가?"를 서버가 판단할 수 있고, 인터뷰에서 "왜 DB에 저장하나?"라는 질문에 답할 근거가 생긴다.

**payment 시점에만 재고를 차감하는 방식.** 폐기 이유: 결제 지연 동안 oversell 위험을 정직하게 다루지 못한다. checkout 시점에 `@Version` 낙관적 락으로 재고를 먼저 예약하면, 결제 전에 이미 재고 경합을 해결한 상태가 된다.

**Kafka publish를 payment 트랜잭션 안에서 직접 호출하는 방식.** 폐기 이유: DB 커밋과 메시지 브로커 전송 사이의 원자성을 보장할 수 없다. outbox 테이블에 이벤트를 DB 트랜잭션과 함께 저장한 뒤, 별도 publisher가 polling하여 Kafka로 전송하면 "DB와 메시지의 일관성을 어떻게 보장하나?"에 답할 수 있다.

**Redis를 product/order read model까지 넓히는 방식.** 폐기 이유: 포트폴리오 범위 대비 캐시 무효화 설명 비용이 너무 크다. Redis는 cart처럼 "DB에 넣기엔 일시적이고, 세션에 넣기엔 영속이 필요한" 영역에만 한정했다.

## 근거 파일

이 선택을 증명하는 핵심 소스 파일은 다음과 같다:

- `OrderService.java` — checkout 트랜잭션: 장바구니 → 주문 생성 + 재고 예약
- `PaymentService.java` — idempotency key 기반 결제 확인 + outbox 이벤트 삽입
- `RedisCartStore.java` — CartStore 인터페이스의 Redis 구현
- `OutboxPublisher.java` — outbox 테이블 polling → Kafka 전송
- `V2__commerce.sql` — 전체 스키마 정의

검증은 `CommercePortfolioApiTest`(전체 흐름 통합 테스트)와 `CommerceMessagingIntegrationTest`(Testcontainers 기반 Kafka 통합 테스트)로 수행했다.
