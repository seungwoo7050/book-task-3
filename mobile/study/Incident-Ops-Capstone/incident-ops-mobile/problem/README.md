# Problem: Incident Ops Mobile Contract Harness

> Status: VERIFIED
> Scope: system contract capstone
> Last Checked: 2026-03-08

## Objective

Preserve the incident-ops backend and shared DTO contract as the canonical source,
and build a small React Native harness that proves the mobile client can interpret that
contract correctly.

## Why This Is Not The Portfolio Client

`incident-ops-mobile` stops at the system boundary.
It covers contract interpretation, approval rules, audit timeline, and replay diagnostics.

The following stay out of scope here and move to `incident-ops-mobile-client`.

- polished product UX
- durable outbox persistence
- offline-first completion
- portfolio/demo packaging

## Required Harness Scope

1. login actor selection
2. incident list rendering
3. operator actions: `ack`, `request-resolution`
4. approver actions: `approve`, `reject`
5. audit timeline rendering
6. websocket replay diagnostics using `lastEventId`

## Canonical Interfaces

- shared DTOs: `problem/code/contracts/contracts.ts`
- backend implementation: `node-server/`
- client harness: `react-native/`

## Evaluation

- `make test`
- `make app-build`
- `make app-test`
- `make server-test`
- `make demo-e2e`

The project is complete only when the contract package, harness, and server all remain reproducible.
