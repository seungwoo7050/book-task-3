# 06 release compatibility와 quality gate 디버그 기록

## 먼저 확인할 명령

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

## 다시 막히기 쉬운 지점

- 상위 `README.md`, `problem/README.md`, `docs/README.md`, 연결된 capstone 경로 설명이 서로 어긋나지 않는지 먼저 확인한다.
- `v2-submission-polish`가 아니라 다른 버전의 코드를 보고 있으면 stage 목적이 흐려질 수 있다.
- 이 단계는 추천 결과를 보여 주는 데서 끝나지 않고, 배포 판단과 제출 산출물까지 연결한다.

## 현재 상태 메모

- compatibility, release gate, artifact export는 `v2`에서 구현돼 최종 제출 proof의 핵심이 된다.
- 이 stage는 운영형 추천 시스템이 '배포 가능한가'를 어떻게 판단하는지 설명한다.

## 재현 실패 시 다시 볼 경로

- `08-capstone-submission/v2-submission-polish/node/src/services/compatibility-service.ts`
- `08-capstone-submission/v2-submission-polish/node/src/services/release-gate-service.ts`
- `08-capstone-submission/v2-submission-polish/node/src/services/artifact-service.ts`
- `08-capstone-submission/v2-submission-polish/node/tests/compatibility-service.test.ts`
- `08-capstone-submission/v2-submission-polish/node/tests/release-gate-service.test.ts`
