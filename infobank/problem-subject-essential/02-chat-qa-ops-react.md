# 02-chat-qa-ops-react 문제지

## 왜 중요한가

평가 결과와 trace를 운영 콘솔에서 어떻게 읽히는 형태로 보여줄 것인가?

## 목표

시작 위치의 구현을 완성해 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다, backend contract와 frontend mocked tests가 같은 payload shape를 공유한다, run label과 retrieval version 같은 lineage 정보가 session review에 노출된다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/api/client.ts`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/App.tsx`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/components/ConversationList.tsx`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/components/FailureTable.tsx`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/App.test.tsx`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/pages/EvalRunner.test.tsx`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/pnpm-lock.yaml`
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/tsconfig.json`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/src/api/client.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 운영자가 평균 점수, failure top, 세션 trace, compare delta를 한 곳에서 읽을 수 있다.
- backend contract와 frontend mocked tests가 같은 payload shape를 공유한다.
- run label과 retrieval version 같은 lineage 정보가 session review에 노출된다.

## 제외 범위

- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/pnpm-lock.yaml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `BASE_URL`와 `apiGet`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `App`와 `renders dashboard title`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react/pnpm-lock.yaml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react && npm run test -- --run`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/07-monitoring-dashboard-and-review-console/react && npm run test -- --run
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-chat-qa-ops-react_answer.md`](02-chat-qa-ops-react_answer.md)에서 확인한다.
