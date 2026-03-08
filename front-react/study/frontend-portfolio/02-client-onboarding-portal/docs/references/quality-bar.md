# Quality Bar

## Command

```bash
cd study
npm run verify --workspace @front-react/client-onboarding-portal
```

## What Is Verified

- unit
  - schema validation
  - draft storage persistence
  - step coercion and submit guard
- integration
  - route guard fallback
  - workspace save -> invite add -> review complete -> submit failure / retry
- E2E
  - direct onboarding access without session
  - sign-in -> validation -> draft restore -> retry -> success

## Notes

- auth, storage, and submit are mock service boundaries다.
- 이 품질 기준의 목표는 realistic frontend flow를 보여 주는 것이지 backend correctness를 주장하는 것이 아니다.
