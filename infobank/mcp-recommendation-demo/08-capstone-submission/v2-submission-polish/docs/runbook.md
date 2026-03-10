# 실행 안내서

## 목표

`v2` 데모는 추천 실험 결과를 릴리즈 후보 승인 흐름으로 연결하는 제출 준비가 끝난 운영 경로를 재현한다.

## 로컬 실행

1. `cp .env.example .env`
2. `pnpm install`
3. `pnpm db:up`
4. `pnpm migrate`
5. `pnpm seed`
6. `pnpm dev`

## 릴리즈 워크플로

1. 대시보드에서 `Candidate 실행` 또는 `Compare 갱신`으로 최신 추천/평가 상태를 확인한다.
2. `Release Candidate Console`에서 후보를 선택하거나 새로 생성한다.
3. `Release Gate 실행`을 눌러 `eval -> compare -> compatibility -> release gate -> artifact export`를 순서대로 실행한다.
4. `Release Quality` 카드에서 `PASS/PENDING`를 확인한다.
5. `Submission Artifact Preview`의 Markdown을 제출 증빙으로 사용한다.

## CLI 경로

```bash
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
```
