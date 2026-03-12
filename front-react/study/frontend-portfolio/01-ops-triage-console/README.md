# Ops Triage Console

상태: `verified`

## 무슨 문제인가

support, QA, customer feedback, monitoring에서 올라온 이슈를 한 명의 운영자가 빠르게 triage하려면 dashboard, dense queue, detail action, bulk update, failure recovery가 한 화면 흐름 안에서 맞물려야 한다. 이 프로젝트는 data-heavy internal tool을 실제 제품처럼 설계하고 검증하는 문제를 푼다.

## 왜 필요한가

이 프로젝트는 React를 사용할 줄 아는 수준을 넘어 "제품형 프론트 결과물로 설명 가능한가"를 보여 준다. 특히 내부도구형 UI, optimistic mutation, retry/undo, 문서화와 발표 자료를 한 번에 묶어 포트폴리오 신호를 만든다.

## 내가 만든 답

dashboard summary, searchable triage queue, saved view, bulk action, optimistic update, rollback, retry, demo reset을 갖춘 Next.js 운영 콘솔을 구현했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [next/README.md](next/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `next/src/components/console/ops-triage-console.tsx`에서 dashboard, queue, bulk workflow를 한 화면 구조로 통합한다.
- `next/src/hooks/use-ops-triage.ts`에서 list/detail query와 mutation, toast, runtime state를 조합한다.
- `next/src/lib/optimistic.ts`, `simulate.ts`, `query.ts`에서 optimistic update, failure simulation, saved view/query 규칙을 분리한다.

## 검증

```bash
cd study
npm run dev --workspace @front-react/ops-triage-console
npm run verify --workspace @front-react/ops-triage-console
```

- 검증 기준일: 2026-03-08
- `typecheck`: `next/tsconfig.json` 기준 타입 검사 통과
- `vitest`: query/filter/sort, optimistic helper, failure simulation, console integration 확인
- `playwright`: dashboard -> queue -> detail -> undo, saved view + bulk update, simulated failure + retry, keyboard flow 확인

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [next/README.md](next/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 실제 인증, 실제 DB, 멀티유저 실시간 협업은 다루지 않는다.
- mock API와 local persistence 기준으로 완결된 데모를 목표로 한다.
- 다음 단계인 `02-client-onboarding-portal`에서 고객-facing form, session gate, multi-step flow를 채운다.
