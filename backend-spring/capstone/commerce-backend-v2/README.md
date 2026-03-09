# commerce-backend-v2

- Status: `verified portfolio capstone`
- Role: N+1 capstone that preserves `commerce-backend/` as the baseline scaffold and upgrades the same domain into a stronger junior Spring backend project
- Spring workspace: [spring/README.md](/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/spring/README.md#L1)
- Notes and architecture docs: [docs/README.md](/Users/woopinbell/work/web-pong/study2/capstone/commerce-backend-v2/docs/README.md#L1)

## Problem

Build a backend-only commerce service that demonstrates the parts Korean junior Spring backend postings repeatedly ask for: persisted auth, JPA-backed domain modeling, PostgreSQL, Redis, idempotent payment handling, one complete Kafka-backed async event flow, Docker, tests, and AWS-oriented deployment notes.

## Scope

- local registration/login plus mocked Google OAuth callback linking
- refresh-token rotation with HttpOnly cookie and CSRF header checks
- admin category/product management and public catalog API
- Redis-backed or in-memory cart, DB-backed orders, optimistic-lock stock reservation
- mock payment confirmation with enforced idempotency keys
- outbox publisher and Kafka consumer for `order-paid` notifications
- health/readiness endpoints, JSON logs, Prometheus metrics, Compose stack, and CI wiring

## Why v2 exists

- `commerce-backend/` is kept intact as the original integrated scaffold
- `commerce-backend-v2/` reuses the same capstone slot but raises the implementation depth to portfolio level
- the goal is not a different domain, but a stronger proof of Spring Boot, JPA, Redis, and operational literacy
