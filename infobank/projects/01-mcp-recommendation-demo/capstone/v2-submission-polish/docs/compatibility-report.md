# 호환성 리포트

`compatibility gate`는 아래 다섯 가지를 deterministic rule로 검사한다.

1. manifest schema 유효성 및 release version 일치 여부
2. target client version이 min/max 범위와 tested set에 포함되는지
3. semver bump와 `breakingChanges` 메타데이터가 일관적인지
4. deprecated field 사용이 없는지
5. 한국어 summary/use case/differentiation/exposure 메타데이터가 비어 있지 않은지

Proof command:

```bash
pnpm compatibility rc-release-check-bot-1-5-0
```
