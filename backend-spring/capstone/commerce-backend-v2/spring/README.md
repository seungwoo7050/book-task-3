# commerce-backend-v2 Spring

- Status: `verified portfolio capstone`
- Problem scope covered: persisted auth, catalog, cart, checkout, mock payment, outbox publishing, Kafka notification consumption, and ops surfaces in one Spring modular monolith

## Commands

- `cp .env.example .env`
- `make run`
- `make lint`
- `make test`
- `make smoke`
- `docker compose up --build`

`make test` now includes a Testcontainers-backed messaging test, so local Docker availability is assumed.

## Implemented

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
- PostgreSQL schema via Flyway
- Redis-backed cart and Redis-backed auth throttling under the Docker profile
- Kafka/Redpanda-backed `order-paid` publication and notification consumption under the Docker profile

## Architecture

- package layout: `auth`, `catalog`, `cart`, `order`, `payment`, `notification`, `global`
- style: single Spring Boot modular monolith, not a microservice split
- persistence: PostgreSQL in Docker, H2 for fast local tests, Redis for cart/rate-limit state
- async: outbox table plus scheduled publisher plus Kafka consumer

## Known tradeoffs

- Google OAuth is contract-level and mocked rather than wired to a live Google console
- payment is deliberately mock-only; the focus is idempotency and order-state control
- the service is portfolio-grade for a junior application, not a production commerce platform
