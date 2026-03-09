# Release Gate Proof

`v3`의 release gate는 더 이상 하드코딩 threshold만 보지 않는다. `Instance Settings`에 저장된 값을 읽어 판정한다.

## Settings Used

- `evalMinTop3Recall`
- `compareMinUplift`
- `defaultLocale`
- `defaultClientVersion`

## Pass Conditions

- compatibility pass
- latest eval가 `evalMinTop3Recall` 이상
- latest compare uplift가 `compareMinUplift` 이상
- required docs와 required artifacts가 workspace에 존재
- release notes가 비어 있지 않음

## Verification

```bash
pnpm release:gate rc-release-check-bot-1-5-0
```

## Last Verified Target

- `passed = true`
- `top3Recall = 0.9583`
- `uplift = 0.1146`
