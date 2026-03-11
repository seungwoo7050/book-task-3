# v2 제출 마감 버전 문제 정의

## 이번 버전의 목표

v1를 바탕으로 compatibility gate, release gate, artifact export, 제출용 proof 문서를 더해 최종 capstone으로 마감한 버전이다.

## 최소 범위

- compatibility gate와 release gate
- artifact export와 제출용 proof 문서
- 최종 시연 runbook과 compare artifact

## 검증 명령

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

## 증빙 산출물

- compare report
- compatibility report
- release gate proof
- presentation capture assets
