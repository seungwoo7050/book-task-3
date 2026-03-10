# Problem Framing — 면접에서 설명 가능한 커머스 백엔드를 만든다

## 이 캡스톤이 존재하는 이유

`commerce-backend`(v1)은 7개 랩의 개념을 하나의 도메인으로 엮는 baseline이었다. 인증은 stub이고, 결제는 없고, 이벤트 연동은 구조만 있었다. 면접에서 "백엔드 프로젝트를 보여주세요"라고 했을 때 v1을 내밀면 "이것은 아직 scaffold입니다"라고 설명해야 한다.

`commerce-backend-v2`는 그 한계를 정면으로 해결한다. 같은 커머스 도메인을 유지하되, 한국 주니어 백엔드 채용 공고에서 자주 요구하는 것들 — Spring Boot, JPA, PostgreSQL, Redis, Docker, 테스트, 인증/인가 — 을 **실제 저장소 기반 흐름**으로 연결한다. 엔드포인트 수를 늘리는 것이 아니라, 각 흐름의 구현 깊이를 면접에서 설명 가능한 수준으로 올리는 것이 목표이다.

## 이 캡스톤이 다루는 것

### 인증과 보안

로컬 인증은 회원가입 → 로그인 → access token(Bearer JWT) + refresh token(HttpOnly cookie) 발급 구조를 따른다. refresh 시 이전 토큰을 폐기하고 새 토큰을 발급하는 rotation을 적용했고, DB에는 토큰 원문이 아닌 hash만 저장한다. refresh/logout 요청에는 CSRF header 검증을 강제하여, 유출된 쿠키만으로는 갱신할 수 없게 만들었다. Google OAuth는 authorize/callback contract를 mock으로 구현하여, 기존 계정 linking 또는 신규 계정 생성 흐름을 증명한다. 실제 Google Console 연동은 제외했다. admin/customer 역할을 분리하여, admin surface는 `/api/v1/admin/**`로 격리했다.

### 카탈로그와 장바구니

admin이 카테고리를 만들고, 카테고리 아래에 상품을 등록한다. 상품 목록은 페이지네이션(`PageResponse`)을 지원한다. 장바구니는 `CartStore` 인터페이스 뒤에 `RedisCartStore`(Docker)와 `InMemoryCartStore`(로컬)를 두어, 실행 환경에 따라 저장소를 교체할 수 있다. `CartState`는 JSON 직렬화되어 Redis에 저장되며, `isEmpty()` 메서드에 `@JsonIgnore`를 붙여 직렬화 계약과 도메인 메서드를 분리했다.

### 주문과 재고

checkout은 장바구니 → 주문 생성 + 재고 예약(stock 차감)을 하나의 트랜잭션으로 묶는다. `@Version` 낙관적 락으로 oversell을 방지한다. 주문 상태는 `PENDING_PAYMENT` → `PAID`로 전이하며, 결제 확인 시 상태가 변경된다. reservation은 checkout 시점에 재고를 먼저 잡고, 결제 미완료 시 해제 가능한 구조를 가진다.

### 결제와 비동기 알림

결제 확인은 Idempotency-Key 헤더를 강제하여 중복 결제를 방지한다. payments 테이블에 idempotency_key를 UNIQUE 제약으로 저장하고, 결제 확인 트랜잭션 안에서 `order-paid` 이벤트를 outbox 테이블에 함께 저장한다. `OutboxPublisher`가 미발행 이벤트를 Kafka로 전송하고, `OrderPaidEventConsumer`가 이를 받아 notification 테이블에 저장한다. `messaging.enabled=true`일 때만 Kafka를 활성화하고, 로컬에서는 동기 fallback으로 notification을 저장한다.

### 운영

health/readiness endpoint, Prometheus 메트릭, JSON structured logging, Trace ID를 포함한다. Docker Compose로 PostgreSQL, Redis, Redpanda, Mailpit을 묶었고, GitHub Actions CI를 구성했다.

## 이 캡스톤이 다루지 않는 것

| 미포함 항목 | 이유 |
|------------|------|
| 실제 Google Console 연동 | OAuth sandbox 설정은 인프라 의존, mock으로 계정 linking 흐름은 충분히 증명 |
| 실제 PG 결제 | PG사 timeout, 중복 callback, 보상 처리는 별도 프로젝트 수준 |
| 쿠폰, 배송, 환불, 정산 | 전체 커머스 도메인이 아닌 "포트폴리오에 필요한 경계"로 제한 |
| AWS 실제 배포 | 배포 방향은 docs에 기록했지만 라이브 검증은 미수행 |
| 장기 운영 안정성 | Kafka consumer 장시간 운영, Redis 장애 대응 등은 미검증 |

## 기술 스택

| 구성 요소 | 선택 |
|----------|------|
| 런타임 | Java 21, Spring Boot 3.4.13 |
| DB | PostgreSQL 16, H2 (로컬/테스트) |
| ORM | Spring Data JPA, Flyway |
| 캐시/상태 | Redis 7 (cart, auth throttling) |
| 메시징 | Redpanda (Kafka 호환), spring-kafka |
| 인증 | JWT (access token), DB-hashed refresh token, CSRF |
| 빌드 | Gradle Kotlin DSL, Spotless (Google Java Format), Checkstyle |
| 테스트 | JUnit 5, MockMvc, Testcontainers (Kafka), H2 |
| 컨테이너 | Docker multi-stage (temurin:21), Docker Compose |

## 성공 기준

- 회원가입 → 로그인 → me 조회
- refresh token rotation → logout
- mocked Google authorize/callback → 계정 link/생성
- admin 카테고리/상품 생성
- cart 추가 → checkout → mock payment confirm → order 조회
- `order-paid` outbox → Kafka consumer → notification 저장
- `make test`, `make lint`, `make smoke` 통과
- 잘못된 CSRF로 refresh/logout 통과 불가
- 중복 Idempotency-Key로 결제 중복 처리 불가
- oversell(재고 음수) 불가

## 불확실한 것들

이 구조가 실제 트래픽 하에서 어느 정도까지 버틸지는 모른다. Kafka consumer를 장시간 돌렸을 때 재처리나 운영 장애가 어떤 형태로 나타날지도 확인하지 않았다. 하지만 주니어 포트폴리오에서는 "모든 인프라를 실서비스 수준으로 운영했다"보다 **"핵심 경계를 왜 이렇게 설계했는지 설명 가능하다"**가 더 중요하다고 가정했다. mocked Google callback도 계정 linking과 persisted auth 흐름을 설명하는 데는 충분하다고 본다. 이 가정은 k6/Locust 부하 테스트, Redis/Kafka 장애 주입 테스트, 실제 AWS 배포로 검증할 수 있다.
