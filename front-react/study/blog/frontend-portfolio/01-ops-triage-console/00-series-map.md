# Ops Triage Console

이 프로젝트의 핵심은 "운영용 대시보드를 만들었다"가 아니라, dense queue, issue detail, bulk action, optimistic rollback, retry, keyboard flow를 한 내부도구 화면 안에서 끝까지 묶었다는 데 있다. 이번 Todo에서는 제품 표면, optimistic mutation 경로, 실패와 복구 검증을 source와 실제 verify 결과 기준으로 다시 정리했다.

## 왜 이 순서로 읽는가

구현 축이 세 갈래로 뚜렷하다.

1. console surface를 어떻게 배치했는가
2. optimistic update와 undo/retry를 어떻게 만들었는가
3. 실패와 keyboard path까지 실제로 버티는가

그래서 본문도 세 편으로 나눠 읽는 편이 맞았다.

## 이번 재작성의 근거

- `frontend-portfolio/01-ops-triage-console/problem/README.md`
- `frontend-portfolio/01-ops-triage-console/docs/README.md`
- `frontend-portfolio/01-ops-triage-console/next/README.md`
- `frontend-portfolio/01-ops-triage-console/next/src/components/console/ops-triage-console.tsx`
- `frontend-portfolio/01-ops-triage-console/next/src/hooks/use-ops-triage.ts`
- `frontend-portfolio/01-ops-triage-console/next/src/lib/optimistic.ts`
- `frontend-portfolio/01-ops-triage-console/next/src/lib/query.ts`
- `frontend-portfolio/01-ops-triage-console/next/src/lib/simulate.ts`
- `frontend-portfolio/01-ops-triage-console/next/tests/unit/*.ts`
- `frontend-portfolio/01-ops-triage-console/next/tests/integration/ops-triage-console.test.tsx`
- `frontend-portfolio/01-ops-triage-console/next/tests/e2e/ops-triage.spec.ts`

## 현재 검증 상태

```bash
npm run verify --workspace @front-react/ops-triage-console
```

- 2026-03-14 재실행 기준 `typecheck` 통과
- `vitest` 16개 테스트 통과
- `playwright` 4개 시나리오 통과

## 본문

- [10-building-the-triage-surface.md](10-building-the-triage-surface.md)
- [20-making-optimistic-actions-reversible.md](20-making-optimistic-actions-reversible.md)
- [30-proving-the-console-under-failure.md](30-proving-the-console-under-failure.md)

## 이번에 명시적으로 남긴 경계

- mock service와 local persistence 위에서 완결되는 데모다.
- saved view는 사용자가 저장하는 서버 객체가 아니라 shipped constant preset이다.
- single-operator 시나리오에 집중하며 multi-user real-time sync는 없다.
- E2E의 `No matching issues`는 전체 시스템 queue가 0건이라는 뜻이 아니라, 현재 필터링된 view 결과가 비었다는 뜻이다.
- retry/undo는 제품형 경험을 보여 주지만 실제 backend transaction 보장은 아니다.
