# Problem: Offline Sync Foundations

> Status: VERIFIED
> Scope: queue/retry/replay foundation
> Last Checked: 2026-03-08

## Objective

RN 앱 내부의 deterministic fake sync service를 사용해
outbox, retry, DLQ, idempotency, pull-after-push merge 규칙을 검증한다.

## Required Scope

1. task create queue
2. retry and DLQ
3. idempotency key handling
4. reconnect flush
5. conflict merge helper

## Evaluation

```bash
make test
make app-build
make app-test
```
