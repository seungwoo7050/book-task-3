# commerce-backend-v2 Problem

Implement a backend-only commerce system that recomposes the Spring labs into one coherent modular monolith, but do it at a depth that is defensible in a junior backend interview.

## Required capabilities

- persisted local auth and mocked Google account linking
- JPA + Flyway + PostgreSQL domain modeling for catalog, orders, payments, and notifications
- Redis-backed state where it is operationally justified
- one complete asynchronous event flow using Kafka/Redpanda
- Docker Compose, health/readiness, metrics, and deployment notes that read like real backend operations work
