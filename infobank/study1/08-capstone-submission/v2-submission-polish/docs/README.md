# v2 Docs

`v2-submission-polish`의 tracked docs index입니다. 운영 절차와 제출 증빙만 남기고, 시행착오와 세부 로그는 `notion/`으로 분리합니다.

## Included

- `runbook.md`: 로컬 데모 부트스트랩과 release gate 실행 순서
- `eval-proof.md`: offline eval acceptance 기준과 기대 결과
- `compare-report.md`: baseline vs candidate compare 기준
- `compatibility-report.md`: semver/compatibility gate 체크 항목
- `release-gate-proof.md`: release gate pass/fail 조건과 artifact 묶음
- `korean-market-fit.md`: 한국어 추천 근거와 운영 적합성 요약
- `presentation-deck.md`: 발표용 시나리오, 실제 캡처 화면, 발표 멘트가 포함된 Markdown deck
- `presentation-assets/`: `pnpm capture:presentation`으로 생성한 데모 화면 캡처

## Commands

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
pnpm capture:presentation
pnpm test
pnpm e2e
```

## Status

- Backend/API: implemented
- Dashboard: implemented
- Compatibility and release gates: implemented
- Dry-run pipeline: implemented via `../../.github/workflows/study1-v2-dry-run.yml`
