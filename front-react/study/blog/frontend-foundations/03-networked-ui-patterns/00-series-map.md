# 03 Networked UI Patterns

이 프로젝트의 핵심은 "목업 API를 붙였다"가 아니라, request lifecycle과 navigation state가 동시에 움직일 때 UI가 어떤 규칙으로 stale response를 버리고 retry를 이어 가는지 설명할 수 있게 만드는 데 있다. 이번 Todo에서는 list/detail 분리 상태, `AbortController`, request token, query-param navigation, retry 후 keyboard continuity를 중심으로 다시 정리했다.

## 왜 이 순서로 읽는가

구현 흐름이 분명하다. `service.ts`가 latency와 failure를 만든 뒤, `state.ts`가 URL/query와 request tracker를 제공하고, `app.ts`가 list/detail loading을 따로 돌리며 stale response를 버린다. 마지막에 브라우저 검증이 navigation과 retry 흐름을 재생한다.

## 이번 재작성의 근거

- `frontend-foundations/03-networked-ui-patterns/problem/README.md`
- `frontend-foundations/03-networked-ui-patterns/docs/README.md`
- `frontend-foundations/03-networked-ui-patterns/docs/references/verification-notes.md`
- `frontend-foundations/03-networked-ui-patterns/vanilla/README.md`
- `frontend-foundations/03-networked-ui-patterns/vanilla/src/app.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/src/service.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/src/state.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/tests/service.test.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.test.ts`
- `frontend-foundations/03-networked-ui-patterns/vanilla/tests/explorer.spec.ts`

## 현재 검증 상태

```bash
npm run build --workspace @front-react/networked-ui-patterns
npm run test --workspace @front-react/networked-ui-patterns
npm run e2e --workspace @front-react/networked-ui-patterns
```

- 2026-03-14 재실행 기준 `vite build` 통과
- `vitest` 4개 테스트 통과
- `playwright` 2개 시나리오 통과

## 본문

- [10-request-lifecycle-in-a-vanilla-explorer.md](10-request-lifecycle-in-a-vanilla-explorer.md)
  - list/detail 비동기 상태를 분리하고, abort와 stale-response 보호를 어떻게 얹었는지 따라간다.

## 이번에 명시적으로 남긴 경계

- 실제 서버 캐시나 인증은 없다.
- stale response 보호는 request token 기반이며, cache revalidation 같은 더 큰 전략은 아직 없다.
- keyboard flow는 retry와 open-item까지 smoke 수준으로만 확인한다.
