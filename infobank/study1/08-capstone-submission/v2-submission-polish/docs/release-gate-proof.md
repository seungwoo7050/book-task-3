# Release Gate Proof

`release gate`는 아래 조건이 모두 맞을 때만 통과한다.

- latest compatibility report가 `passed=true`
- latest offline eval acceptance가 모두 true
- latest compare uplift가 `0.02` 이상이고 baseline 이하로 떨어지지 않음
- seeded required docs/artifacts가 실제 파일로 존재함
- release note에 `변경 요약`, `검증`, `리스크` 섹션이 포함됨

Proof command:

```bash
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
```
