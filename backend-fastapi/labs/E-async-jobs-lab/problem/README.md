# Problem

Build a backend slice that accepts notification jobs, stores them safely, and hands them off to background execution.

The lab should demonstrate:

- idempotency keys on write endpoints
- outbox persistence before dispatch
- Celery task invocation
- retry-aware status transitions
- local Redis-backed configuration
