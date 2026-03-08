# Ops Triage Console

상태: `verified`

`Ops Triage Console`은 support, QA, customer feedback, monitoring에서 올라온 이슈를 한 명의 운영자가 빠르게 triage하도록 돕는 B2B 운영 콘솔이다.

## 왜 주니어 경로에 필요한가

이 프로젝트는 데이터가 많은 내부도구 UI, async mutation, retry/undo, 테스트와 발표 문서를 한 번에 보여 준다. 즉, React를 사용할 줄 안다는 수준을 넘어 "제품형 프론트 결과물로 설명 가능한가"를 증명하는 프로젝트다.

## Prerequisite

- 라우팅과 컴포넌트 구조 기초
- 비동기 상태와 optimistic update 개념
- form, table, dialog 같은 제품 UI 조합 경험

## 이 프로젝트가 보여 주려는 것

- 제품형 프론트 앱 설계와 화면 밀도 제어
- 필터, 정렬, saved view, bulk action이 있는 data-heavy UI
- optimistic update, rollback, retry, undo 흐름
- 접근성과 keyboard flow를 고려한 상호작용
- unit, integration, E2E를 포함한 검증 체계

## 구조

- `problem/`: authored product brief와 입력 데이터 자리
- `next/`: 실제 Next.js 앱, 소스, 테스트
- `docs/`: case study, 발표 자료, 설계 문서
- `notion/`: 로컬 전용 작업 로그와 회고

## 빠른 실행

```bash
cd study
npm run dev:portfolio
```

## 검증

```bash
cd study
npm run verify:portfolio
```

## 주요 화면

- Dashboard: queue health, SLA risk, priority distribution, recent changes
- Queue: search, faceted filters, saved views, bulk select, table workflow
- Issue Detail: timeline, metadata, notes, triage actions
- Case Study: 제품 요약, UX 판단, 테스트/성능 요약

## 보조 학습 근거

`react-internals` 트랙은 이 앱을 설명하기 위한 참고 자료일 뿐, 이 프로젝트의 실행 경로는 아니다.

## 다음 프로젝트로 이어지는 한계

이 앱은 내부 운영 콘솔에 강하지만 고객-facing form, session gate, multi-step onboarding 흐름은 다루지 않는다. 그 축은 `02-client-onboarding-portal`이 채운다.
