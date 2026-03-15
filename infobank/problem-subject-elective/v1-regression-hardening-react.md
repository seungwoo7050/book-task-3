# v1-regression-hardening-react 문제지

## 왜 중요한가

v1-regression-hardening은 v0-initial-demo를 바탕으로 회귀 검증, provider fallback, lineage 노출, PostgreSQL smoke path를 강화한 버전이다. "데모가 한 번 돌아간다"를 넘어서 "개선 여부를 비교하고 운영 경로를 점검할 수 있다"까지 끌어올리는 것이 목표다.

## 목표

v0를 바탕으로 회귀 안정성과 lineage를 강화해, 개선 실험이 실제로 나아졌는지 비교 가능한 상태를 만든다.

## 시작 위치

- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/api/client.ts`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/App.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/ConversationList.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/components/FailureTable.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/App.test.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/pages/EvalRunner.test.tsx`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/pnpm-lock.yaml`
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/tsconfig.json`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/api/client.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- version compare
- regression coverage 확대
- fallback 안정화
- lineage/trace 노출

## 제외 범위

- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/pnpm-lock.yaml` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `BASE_URL`와 `apiGet`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `App`와 `renders dashboard title`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/pnpm-lock.yaml` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/react && npm run test -- --run`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/capstone/v1-regression-hardening/react && npm run test -- --run
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`v1-regression-hardening-react_answer.md`](v1-regression-hardening-react_answer.md)에서 확인한다.
