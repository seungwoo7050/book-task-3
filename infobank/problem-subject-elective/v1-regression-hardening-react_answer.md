# v1-regression-hardening-react 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

v0를 바탕으로 회귀 안정성과 lineage를 강화해, 개선 실험이 실제로 나아졌는지 비교 가능한 상태를 만든다. 핵심은 `BASE_URL`와 `apiGet`, `apiPost` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- version compare
- regression coverage 확대
- fallback 안정화
- 첫 진입점은 `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/api/client.ts`이고, 여기서 `BASE_URL`와 `apiGet` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/api/client.ts`: `BASE_URL`, `apiGet`, `apiPost`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/App.tsx`: `App`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/ConversationList.tsx`: `ConversationList`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/FailureTable.tsx`: `FailureTable`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/ScoreCard.tsx`: `ScoreCard`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/App.test.tsx`: `App`, `renders dashboard title`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/pages/EvalRunner.test.tsx`: `EvalRunnerPage`, `submits golden-set runs with run metadata and renders the summary`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/pages/Failures.test.tsx`: `FailuresPage`, `renders failure aggregates from the dashboard API`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/api/client.ts`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `App` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/react && npm run test -- --run`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/react && npm run test -- --run
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `App`와 `renders dashboard title`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/react && npm run test -- --run`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/api/client.ts`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/App.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/ConversationList.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/FailureTable.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/ScoreCard.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/App.test.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/pages/EvalRunner.test.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/pages/Failures.test.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/pnpm-lock.yaml`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/tsconfig.json`
