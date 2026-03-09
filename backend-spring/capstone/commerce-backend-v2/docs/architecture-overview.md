# Architecture Overview

`commerce-backend-v2` is a Spring Boot modular monolith. The goal is to keep the codebase interview-readable while still showing the boundaries a junior backend engineer is expected to reason about.

## Modules

- `auth`: users, roles, refresh tokens, mocked Google account linking, audit events, JWT issuance, refresh rotation
- `catalog`: categories and products, admin write APIs, public read APIs, optimistic-lock stock field
- `cart`: user cart state behind a `CartStore` interface with in-memory and Redis implementations
- `order`: checkout, order state transitions, order items, inventory reservations
- `payment`: mock payment confirmation with mandatory idempotency keys
- `notification`: outbox table, publisher, Kafka consumer, user notification records
- `global`: security, error envelope, health, OpenAPI, trace ID logging

## Core request flow

1. User registers or logs in.
2. Access token is sent as Bearer token. Refresh token is kept in an HttpOnly cookie.
3. Customer adds products to cart.
4. Checkout reserves stock and creates `orders`, `order_items`, and `inventory_reservations`.
5. Mock payment confirmation moves the order to `PAID`, stores a `payments` row, and writes an `outbox_events` record.
6. The outbox publisher sends the `order-paid` event to Kafka.
7. The consumer stores a `notifications` row and a supporting audit event.

## Why this shape

- It shows boundary design without forcing microservice infrastructure.
- It keeps Redis and Kafka as implementation details of justified features, not buzzwords.
- It is small enough to explain in an interview and large enough to prove backend judgment.

