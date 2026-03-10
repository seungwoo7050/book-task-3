# Timeline — 소스코드에서는 드러나지 않는 것들

## Docker Compose 환경 구성

이 캡스톤의 Docker 환경은 다른 랩들보다 복잡하다. `compose.yaml`에 다섯 개 서비스가 정의되어 있다:

```bash
docker compose up -d
# app (Spring Boot, multi-stage build, temurin:21)
# postgres (PostgreSQL 16, healthcheck 포함)
# redis (Redis 7)
# mailpit (v1.24, SMTP + UI)
# redpanda (v24.3.8, Kafka 호환 broker)
```

PostgreSQL은 `service_healthy` 조건으로 앱 시작 전 준비 완료를 보장한다. Redis, Mailpit, Redpanda는 `service_started`로 설정되어 있다. 환경 변수는 `.env` 파일과 compose 기본값을 조합한다.

```
POSTGRES_DB=commerce_backend_v2
POSTGRES_USER=study2
SERVER_PORT=8111 (외부) → 8080 (내부)
KAFKA_BOOTSTRAP_SERVERS=redpanda:9092
KAFKA_PORT=19091 (외부) → 19092 (내부)
```

Redpanda는 단일 노드, 512M 메모리, overprovisioned 모드로 경량 실행한다. Kafka 호환 프로토콜을 제공하므로 spring-kafka가 그대로 연결된다.

## Flyway 마이그레이션

두 개의 migration 파일이 존재한다:

- `V1__init.sql` — `study2_marker` 테이블. 공통 scaffold marker.
- `V2__commerce.sql` — 전체 도메인 스키마. 12개 테이블 정의:

```
users, user_roles, refresh_tokens, oauth_accounts, audit_events,
categories, products, orders, order_items, inventory_reservations,
payments, outbox_events, notifications
```

`V2__commerce.sql`은 이 캡스톤의 핵심이다. 주요 설계 결정이 DDL에 반영되어 있다:
- `refresh_tokens.token_hash` — 원문 대신 hash 저장
- `products.version` — `@Version` 낙관적 락
- `payments.idempotency_key UNIQUE` — 중복 결제 방지
- `outbox_events.published_at` — NULL이면 미발행
- `notifications.dedup_key UNIQUE` — 중복 알림 방지

H2 환경에서는 Flyway가 같은 스크립트를 실행하되, PostgreSQL 전용 문법 없이 호환되도록 DDL을 작성했다.

## Docker 멀티스테이지 빌드

```dockerfile
FROM eclipse-temurin:21-jdk AS build    # 빌드 스테이지
FROM eclipse-temurin:21-jre             # 런타임 스테이지 (JRE만)
```

빌드 스테이지에서 `./gradlew bootJar`를 실행하고, 런타임 스테이지에는 `app.jar`만 복사한다. JDK 의존성이 런타임 이미지에 포함되지 않으므로 이미지 크기가 줄어든다.

## Makefile 명령어

```bash
make run    # SPRING_PROFILES_ACTIVE=local ./gradlew bootRun
make lint   # spotlessCheck + checkstyleMain + checkstyleTest
make test   # ./gradlew test (Testcontainers 포함, Docker 필요)
make smoke  # ./gradlew test --tests '*SmokeTest'
```

`make test`는 `CommerceMessagingIntegrationTest`를 포함하므로 Docker가 실행 중이어야 한다. Testcontainers가 Kafka 브로커를 별도로 띄운다.

## 프로파일 전략

| 프로파일 | 데이터 저장소 | Redis | Kafka |
|---------|-------------|-------|-------|
| `local` | H2 in-memory | InMemoryCartStore | messaging.enabled=false, 동기 fallback |
| `docker` | PostgreSQL 16 | RedisCartStore | Redpanda, messaging.enabled=true |
| test | H2 in-memory | InMemoryCartStore (기본), RedisCartStore (RedisCartStoreTest) | Testcontainers (CommerceMessagingIntegrationTest) |

`FeatureProperties`와 `MessagingProperties`로 Kafka 활성/비활성을 제어한다. 로컬에서는 Kafka 없이도 전체 흐름이 동작하되, notification은 동기 방식으로 저장된다.

## JWT 설정

`AuthProperties`로 JWT 시크릿, access token TTL, refresh token TTL을 관리한다. 로컬/테스트에서는 application.yml에 기본값을 넣고, Docker 환경에서는 환경 변수로 주입한다.

## Git 이력에서 확인 가능한 것들

소스코드만으로는 보이지 않지만 Git 이력에서 드러나는 결정들:

- `UserRoleEntity`에 `createdAt` 필드가 추가된 커밋 — V2 migration과 entity의 계약 불일치를 수정
- `CartState.isEmpty()`에 `@JsonIgnore`가 붙은 커밋 — Jackson 직렬화 충돌 수정
- `@KafkaListener` groupId가 placeholder에서 고정 문자열로 변경된 커밋 — Testcontainers 환경 호환성 수정
- `spotlessApply` 실행 후 대량 포맷 정리 커밋 — 기능 구현 후 일괄 포맷팅

## Compose 검증

```bash
./tools/compose_probe.sh study2/capstone/commerce-backend-v2/spring 8111
```

이 스크립트는 health/readiness probe로 서비스 상태를 확인한다. 도메인 시나리오(회원가입 → 주문 → 결제)까지 자동 검증하지는 않는다. 전체 흐름 검증은 `CommercePortfolioApiTest`가 담당한다.
