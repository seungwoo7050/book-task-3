# 03 Networked UI Patterns

loading, empty, error, retry, abort, stale response를 vanilla explorer UI에 올려 request lifecycle을 제품처럼 다룬 프로젝트다. 여기서 중요한 건 실제 서버가 아니라 "어떤 응답이 지금 화면을 바꿀 자격이 있는가"라는 규칙이다.

## 왜 이 순서로 읽는가

이 프로젝트는 mock service 설계, latest-request invariant, browser-level recovery proof라는 세 단계를 차례대로 밟는다. 구현 축이 선명해서 본문도 한 편으로 충분하다.

## 근거로 사용한 자료

- `frontend-foundations/03-networked-ui-patterns/README.md`
- `frontend-foundations/03-networked-ui-patterns/docs/concepts/request-lifecycle.md`
- `frontend-foundations/03-networked-ui-patterns/vanilla/src/service.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/src/state.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/tests/service.test.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.spec.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/networked-ui-patterns`
- 2026-03-13 replay 기준 `vitest` 4개, `playwright` 2개 시나리오 통과

## 본문

- [10-request-lifecycle-in-a-vanilla-explorer.md](10-request-lifecycle-in-a-vanilla-explorer.md)
  - abort와 stale-response 방지가 왜 서로 다른 invariant인지, 그리고 그 둘이 UI를 어떻게 안정시켰는지 따라간다.
