# 비교 리포트

- Baseline: `weighted-baseline-v0`
- Candidate: `signal-rerank-v1`
- Source signals: usage CTR, accept rate, operator feedback, explanation quality, freshness
- Gate threshold:
  - `candidateNdcg3 >= baselineNdcg3`
  - `uplift >= 0.02`
- Proof command: `POST /api/compare/run` 또는 `pnpm release:gate rc-release-check-bot-1-5-0` 전에 `pnpm eval`
