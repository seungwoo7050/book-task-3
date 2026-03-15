# v2-submission-polish-react 문제지

## 왜 중요한가

v1를 바탕으로 compatibility gate, release gate, artifact export, 제출용 proof 문서를 더해 최종 capstone으로 마감한 버전이다.

## 목표

시작 위치의 구현을 완성해 compatibility gate와 release gate, artifact export와 제출용 proof 문서, 최종 시연 runbook과 compare artifact를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/app/layout.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/app/page.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/next.config.ts`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.test.tsx`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/tsconfig.json`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/package.json`
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/vitest.config.ts`

## starter code / 입력 계약

- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/app/layout.tsx`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- compatibility gate와 release gate
- artifact export와 제출용 proof 문서
- 최종 시연 runbook과 compare artifact
- compare report

## 제외 범위

- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/tsconfig.json` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `metadata`와 `apiBaseUrl`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `fetchMock`와 `MpcDashboard v2`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/tsconfig.json` fixture/trace 기준으로 결과를 대조했다.
- `pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm eval && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation && pnpm test && pnpm e2e`가 통과한다.

## 검증 방법

```bash
pnpm install && cp .env.example .env && pnpm db:up && pnpm migrate && pnpm seed && pnpm eval && pnpm compatibility rc-release-check-bot-1-5-0 && pnpm release:gate rc-release-check-bot-1-5-0 && pnpm artifact:export rc-release-check-bot-1-5-0 && pnpm capture:presentation && pnpm test && pnpm e2e
```

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react && npm run test
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`v2-submission-polish-react_answer.md`](v2-submission-polish-react_answer.md)에서 확인한다.
