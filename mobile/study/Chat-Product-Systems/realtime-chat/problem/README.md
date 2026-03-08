# Problem: Realtime Chat

> Status: VERIFIED
> Scope: local-first chat model
> Last Checked: 2026-03-08

## Objective

offline send, ack reconcile, replay from `lastEventId`, typing/presence update를
하나의 local-first message model로 검증한다.

## Required Scope

1. pending message creation
2. server ack reconciliation
3. replay dedupe
4. typing and presence update
5. WatermelonDB-style schema definition

## Evaluation

```bash
make test
make app-build
make app-test
```
