# React Native Implementation

Status: verified

이 앱은 incident-ops domain을 설명하는 contract harness다.
실제 제품 완성도는 `incident-ops-mobile-client`에서 다루고, 여기서는 DTO 해석과
상태 전이 규칙을 작은 RN surface로 확인한다.

## Stack

- React Native CLI + TypeScript
- shared contract package `@incident-ops/contracts`

## Commands

```bash
npm install
npm run typecheck
npm test
npm run verify
```

## Covered Behaviors

- login actor selection
- incident status transition harness
- approval decision flow
- audit timeline rendering
- replay diagnostics summary
