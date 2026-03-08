# 06 Release Compatibility And Quality Gates

## Purpose

semver/compatibility gate와 release gate를 deterministic rule로 구현한다.

## Capstone Connection

- `08-capstone-submission/v2-submission-polish/node/src/services/compatibility-service.ts`
- `08-capstone-submission/v2-submission-polish/node/src/services/release-gate-service.ts`
- `08-capstone-submission/v2-submission-polish/node/src/services/artifact-service.ts`

## Main Outputs

- release candidate model
- compatibility report
- release gate report
- artifact export

## Implementation Pointers

- `08-capstone-submission/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `08-capstone-submission/v2-submission-polish/node/tests/release-gate-service.test.ts`

## Status

- implemented in v2
