# 문제 인식 — 왜 Ops Triage Console인가

## react-internals에서 portfolio로

react-internals 트랙에서는 "React가 어떻게 동작하는가"를 직접 구현하며 답했다. 하지만 채용 면접에서 듣는 질문은 다르다. "이 사람한테 제품형 프론트 업무를 맡길 수 있는가?" 이 질문에 답하려면 runtime을 만든 경험이 아니라 제품을 만든 결과가 필요하다.

## 왜 B2B 운영 콘솔인가

consumer UI(이커머스, SNS)를 만들면 비주얼은 화려해지지만, 보여 줄 수 있는 엔지니어링 판단은 제한적이다. 반면 B2B 운영 콘솔은 데이터 밀도, 필터/정렬/검색, 상태 전이, 오류 복구, 접근성 — 이 모든 것을 한 화면에 담아야 한다.

이 도메인을 택한 이유:
- 테이블, 필터, 상태 전이, 정보 밀도, 오류 복구를 한 번에 보여 줄 수 있다
- "예쁜 데모"가 아니라 "업무 흐름을 설계한 결과물"이라는 인상을 줄 수 있다
- 한 화면에서 여러 종류의 품질 문제를 다루므로 우선순위 판단과 UX 구조화 능력이 드러난다

## 사용자와 시나리오

한 명의 운영자가 네 채널(support, QA, customer feedback, monitoring)에서 올라온 이슈를 한곳에서 분류한다. 핵심 질문 세 가지:
1. **무엇을 우선 처리할지** — priority, SLA risk, status로 결정
2. **어느 팀으로 보낼지** — route team 지정, bulk action
3. **잘못된 변경을 어떻게 복구할지** — optimistic update → rollback → retry → undo

## 이 프로젝트가 보여 주는 역량

- query/filter/sort/pagination 모델링 (IssueQuery 타입 + applyIssueQuery 로직)
- async 상태 관리 (React Query, 서버 상태와 UI 상태 분리)
- optimistic update와 rollback (onMutate → 캐시 교체, onError → 캐시 복원)
- retry와 undo (toast action으로 재시도/원복)
- saved view (반복 작업 단축)
- bulk action (다중 선택 + 일괄 변경)
- dense but calm한 UI 톤 (정보는 많지만 시각적으로 차분한 디자인)
- unit/integration/E2E 3레이어 테스트
- 발표 문서와 case study 라우트

## 기술 스택 선택

| 도구 | 이유 |
|------|------|
| Next.js 16 + App Router | 실무 표준, SSR과 라우팅 |
| React 19 | 최신 버전, useDeferredValue 등 |
| TanStack React Query | 서버 상태 관리, optimistic update |
| TanStack React Table | headless table, column 정의 |
| Radix UI | 접근성 보장된 primitives (dialog, select, checkbox, popover, tooltip) |
| Tailwind CSS 4 | 빠른 스타일링, 일관된 디자인 토큰 |
| Zod 4 | 런타임 스키마 검증 (patch 데이터) |
| Playwright | E2E 테스트 |
| Vitest + Testing Library | 단위/통합 테스트 |

## 범위

다루는 것:
- Dashboard (queue health, SLA risk, priority distribution, recent changes)
- Queue (search, faceted filters, saved views, bulk select, table workflow)
- Issue Detail (timeline, metadata, notes, triage actions)
- Case Study 라우트 (제품 요약, UX 판단, 테스트/성능 요약)
- 실패 시뮬레이션 (runtime controls → failure injection)

다루지 않는 것:
- 실제 backend API (mock 서비스 + localStorage)
- 인증/권한
- 고객-facing form, session gate, onboarding (→ 02-client-onboarding-portal)
