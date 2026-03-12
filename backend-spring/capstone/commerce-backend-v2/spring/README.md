# commerce-backend-v2 Spring 워크스페이스

- 상태: `verified portfolio capstone`
- 현재 범위: persisted auth, catalog, cart, checkout, mock payment, outbox publishing, Kafka notification consumption, ops surface

## 실행과 검증 명령

```bash
cp .env.example .env
make run
make lint
make test
make smoke
docker compose up --build
```

`make test`에는 Testcontainers-backed messaging test가 포함되므로 로컬 Docker가 필요하다.

## 현재 구현 요소

- `/api/v1/auth/register`, `login`, `refresh`, `logout`, mocked Google `authorize` and `callback`
- `/api/v1/me`
- `/api/v1/products`
- `/api/v1/admin/categories`
- `/api/v1/admin/products`
- `/api/v1/cart/items`
- `/api/v1/orders`
- `/api/v1/orders/{orderId}`
- `/api/v1/payments/mock/confirm`
- `/api/v1/admin/orders/{orderId}/status`
- Flyway 기반 PostgreSQL schema
- Docker profile에서의 Redis cart / auth throttling
- Docker profile에서의 outbox publisher + Kafka consumer

## 아키텍처 요약

- 패키지 경계: `auth`, `catalog`, `cart`, `order`, `payment`, `notification`, `global`
- 구조: microservice가 아니라 single Spring Boot modular monolith
- persistence: Docker profile의 PostgreSQL, fast test를 위한 H2, 선택적 Redis 사용
- async: outbox table + scheduled publisher + Kafka consumer

## 현재 한계

- Google OAuth는 live provider가 아니라 contract-level mock이다
- payment는 idempotency와 상태 전이 설명을 위한 mock-only다
- 포트폴리오용 학습 결과물이지 production commerce platform을 주장하지 않는다
