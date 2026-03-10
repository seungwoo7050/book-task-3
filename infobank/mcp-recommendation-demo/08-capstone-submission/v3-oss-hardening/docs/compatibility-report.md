# 호환성 리포트

compatibility gate는 release candidate와 catalog manifest를 읽어 아래 항목을 검사한다.

## 검사 항목

- manifest schema validity
- supported runtime range
- breaking semver bump consistency
- deprecated field usage
- required Korean metadata completeness

## 검증

```bash
pnpm compatibility rc-release-check-bot-1-5-0
```

## 마지막 검증 대상

- `passed = true`
- 모든 seeded check가 `PASS`
