# v2 제출 마감 버전

v1를 바탕으로 compatibility gate, release gate, artifact export, 제출용 proof 문서를 더해 최종 capstone으로 마감한 버전이다.

## 이번 버전에서 보여 주는 것

- release candidate CRUD
- compatibility gate
- release gate
- artifact export
- changesets + GitHub Actions dry-run

## 실행 명령

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

## 먼저 확인할 문서

- `docs/runbook.md`
- `docs/eval-proof.md`
- `docs/compare-report.md`
- `docs/compatibility-report.md`
- `docs/release-gate-proof.md`
- `docs/korean-market-fit.md`
- `docs/presentation-deck.md`
- `problem/README.md`

## 현재 상태

- 최종 제출용 capstone 버전으로 정리돼 있다.
- 추천 품질 개선과 release 판단, 제출 산출물 재생성을 한 흐름으로 보여 준다.
