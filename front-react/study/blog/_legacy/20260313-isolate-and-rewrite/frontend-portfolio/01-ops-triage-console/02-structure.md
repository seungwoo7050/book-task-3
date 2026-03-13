# 01 Ops Triage Console structure

## opening frame

- 한 줄 훅: 이 프로젝트의 핵심은 복잡한 UI 조각이 아니라, 한 명의 operator가 dense queue를 끝까지 triage할 수 있게 만드는 workflow contract다.
- chronology 주의: 구현 양은 크지만 판단 전환점은 optimistic mutation과 dense queue orchestration 쪽에 몰려 있다.
- 첫 질문: dashboard, queue, bulk action, rollback, retry를 한 콘솔 안에서 어떻게 일관된 operator 흐름으로 묶었는가.

## chapter flow

1. README와 problem 문서로 운영 콘솔의 public contract를 먼저 고정한다.
2. `useIssueMutation`으로 optimistic update/rollback/undo 파이프라인을 설명한다.
3. `OpsTriageConsole`과 verify 결과로 saved view, bulk update, keyboard triage를 닫는다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log`
- 본문 1: `next/src/hooks/use-ops-triage.ts`
- 본문 2: `next/src/components/console/ops-triage-console.tsx`
- 본문 3: `npm run verify --workspace @front-react/ops-triage-console`, `next/tests/e2e/ops-triage.spec.ts`

## tone guardrails

- "Next.js로 만들었다" 수준의 기술 스택 요약으로 흐르지 않는다.
- optimistic update는 캐시 patch와 rollback/undo까지 같이 설명한다.
- presentation asset은 보조 근거로만 두고, 코드와 tests를 본문 중심에 둔다.
