# Interview Talking Points

## Why a modular monolith instead of microservices

- junior candidates are usually evaluated on transaction boundaries, modeling, and failure handling before service decomposition
- the project keeps operational complexity proportional to the learning goal
- Redis and Kafka are still present, but only where they solve a concrete problem

## Why checkout reserves stock before payment

- it prevents overselling during the payment window
- it gives a concrete place to discuss optimistic locking and compensation
- it keeps the order state machine explicit

## Why refresh tokens are hashed server-side

- stolen database rows do not immediately expose valid refresh tokens
- revocation and rotation can still be implemented with lookup by hash
- it mirrors the same reasoning used for password hashing, with different lifetimes

## Why the project uses an outbox table

- publishing directly to Kafka inside the payment request would blur transaction boundaries
- the outbox keeps DB state as the source of truth
- the publisher and consumer let you discuss eventual consistency without hand-waving

## Why Redis is used selectively

- cart and login throttling are stateful, fast-changing concerns
- product, order, and payment truth stays in PostgreSQL
- this is easier to defend than “we used Redis everywhere”

