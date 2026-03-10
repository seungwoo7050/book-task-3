# v3 문서 안내

이 폴더는 `v3-oss-hardening`을 self-hosted OSS 후보로 이해하는 데 필요한 stable 문서를 모은다. 설치, 보안, 운영, 백업, proof 문서를 먼저 읽고, 시행착오와 장문의 회고는 `notion/`에서 이어서 보면 된다.

## 핵심 운영 문서

- `install.md`: local/compose 설치 경로
- `security-model.md`: auth, session, role, single-workspace boundary
- `operations.md`: bootstrap, seed account, jobs, metrics, audit 운영 절차
- `api.md`: public HTTP contract summary
- `backup-restore.md`: Postgres dump/restore와 bundle export 전략
- `oss-positioning.md`: 누구를 위한 OSS인지와 비범위

## 증빙 문서

- `runbook.md`: 실제 사용 시나리오와 데모 순서
- `eval-proof.md`: offline eval acceptance 기준과 현재 결과
- `compare-report.md`: baseline vs candidate compare 요약
- `compatibility-report.md`: semver/compatibility gate 체크 구조
- `release-gate-proof.md`: release gate threshold와 pass/fail 조건
- `korean-market-fit.md`: 한국어 추천 근거와 운영 시나리오 적합성

## 발표 자료

- `presentation-deck.md`: 발표용 deck
- `presentation-assets/`: `pnpm capture:presentation`으로 생성한 실제 사용 화면 캡처

## 자주 쓰는 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
pnpm build
pnpm test
pnpm test:integration
pnpm e2e
pnpm compare
pnpm capture:presentation
```
