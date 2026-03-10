# 평가 증빙

- Offline eval dataset: `shared/src/eval.ts`
- Case count: 12
- Acceptance:
  - `top3Recall >= 0.90`
  - `explanationCompleteness = 1.00`
  - `forbiddenHitRate = 0.00`
- Proof command: `pnpm eval`
- Expected seeded outcome: `release-check-bot`, `korean-docs-search`, `incident-log-analyst` 계열 질의가 top-3 recall을 유지한다.
