# MCP 추천 Verification Matrix

| 대상 | 목적 | 명령 |
| --- | --- | --- |
| `capstone/v2-submission-polish` | 공식 제출 답 DB 준비 | `pnpm db:up && pnpm migrate && pnpm seed` |
| `capstone/v2-submission-polish` | 공식 제출 답 검증 | `pnpm test` |
| `capstone/v2-submission-polish` | offline eval 재현 | `pnpm eval` |
| `capstone/v2-submission-polish` | compatibility gate | `pnpm compatibility rc-release-check-bot-1-5-0` |
| `capstone/v2-submission-polish` | release gate | `pnpm release:gate rc-release-check-bot-1-5-0` |
| `capstone/v3-oss-hardening` | 확장 버전 회귀 | `pnpm test` |
| `stages/04-selector-baseline-and-reranking` | 개선 로직 학습 포인트 확인 | `v1-ranking-hardening/node/tests/rerank-service.test.ts` 참조 |
