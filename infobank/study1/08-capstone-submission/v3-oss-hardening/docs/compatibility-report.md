# Compatibility Report

compatibility gate는 release candidate와 catalog manifest를 읽어 아래 항목을 검사한다.

## Checks

- manifest schema validity
- supported runtime range
- breaking semver bump consistency
- deprecated field usage
- required Korean metadata completeness

## Verification

```bash
pnpm compatibility rc-release-check-bot-1-5-0
```

## Last Verified Target

- `passed = true`
- 모든 seeded check가 `PASS`
