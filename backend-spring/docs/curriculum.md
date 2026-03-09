# study2 Curriculum

`study2/` is designed as a Spring-first backend learning program rather than a translation of the FastAPI track.

## Sequence

1. `A-auth-lab`: local authentication, refresh rotation, email verification, reset flows
2. `B-federation-security-lab`: Google OAuth2, account linking, 2FA, audit and throttling
3. `C-authorization-lab`: invitations, RBAC, ownership and method security
4. `D-data-jpa-lab`: JPA mapping, Querydsl search, pagination, optimistic locking
5. `E-event-messaging-lab`: outbox pattern, Kafka publishing, retries and DLQ thinking
6. `F-cache-concurrency-lab`: Redis caching, idempotency, reservation concurrency, distributed lock patterns
7. `G-ops-observability-lab`: Compose, health, metrics, logs, CI, deployment notes
8. `capstone/commerce-backend`: preserved baseline modular-monolith scaffold
9. `capstone/commerce-backend-v2`: N+1 portfolio upgrade with persisted auth, Redis cart, idempotent payments, and one complete Kafka-backed event flow

## Hiring signal emphasis

This track leans toward concepts that are repeatedly visible in Korean backend hiring requirements:

- Spring Security and authentication flows
- JPA-centric persistence and search
- PostgreSQL and Redis
- event-driven background processing
- API reliability concerns such as idempotency and locking
- operational basics such as health checks, metrics, Docker, CI, and AWS deployment documentation

## Pedagogical rule

Each lab is independently runnable. The capstones do not import lab code. They re-implement the same ideas in a single commerce backend so the final project reads as one coherent system instead of a stitched demo.
