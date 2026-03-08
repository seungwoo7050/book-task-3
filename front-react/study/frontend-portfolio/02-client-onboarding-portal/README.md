# 02 Client Onboarding Portal

상태: `verified`

`Client Onboarding Portal`은 SaaS 고객의 sign-in, workspace setup, member invite, review and submit 흐름을 다루는 고객-facing onboarding 앱이다.

## 왜 주니어 경로에 필요한가

`Ops Triage Console`은 내부도구형 UI에는 강하지만, 고객-facing form, validation, session gate, multi-step flow는 보여 주지 않는다. 이 프로젝트는 그 폭을 채워 "내부도구 + 고객-facing 제품" 두 축을 함께 갖춘 포트폴리오를 만든다.

## Prerequisite

- `frontend-foundations` 트랙의 DOM/async 기초
- React 컴포넌트와 라우팅 기초
- form validation 개념

## 구조

- `problem/`: authored product brief와 입력/스크립트 자리
- `next/`: Next.js App Router 구현 자리
- `docs/`: 발표 자료와 flow/품질 문서
- `notion/`: 로컬 전용 작업 로그

## Build/Test Command

```bash
cd study
npm run dev --workspace @front-react/client-onboarding-portal
npm run typecheck --workspace @front-react/client-onboarding-portal
npm run test --workspace @front-react/client-onboarding-portal
npm run e2e --workspace @front-react/client-onboarding-portal
npm run verify --workspace @front-react/client-onboarding-portal
```

검증 범위는 아래와 같다.

- sign-in / session gate
- workspace validation과 draft restore
- invite creation
- review checklist와 submit failure -> retry -> success

## 다음 단계로 이어지는 한계

이 프로젝트가 추가되면 `frontend-portfolio` 트랙은 내부도구형과 고객-facing 흐름을 모두 갖추게 된다. 그 이후 확장은 폭을 늘리기보다 문서와 polish를 다듬는 방향이 더 중요해진다.
