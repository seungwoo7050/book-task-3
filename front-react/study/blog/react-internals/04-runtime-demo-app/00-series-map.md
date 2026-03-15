# 04 Runtime Demo App

이 프로젝트의 핵심은 "작은 앱을 만들었다"가 아니라, 앞에서 만든 runtime을 복사하지 않고 실제 consumer app으로 가져와 어디까지 버티는지 드러내는 데 있다. 이번 Todo에서는 shared runtime consumption, debounced query, visible window pagination, metrics panel의 학습용 성격을 중심으로 다시 정리했다.

## 왜 이 순서로 읽는가

이 단계는 구현 자체보다 소비 방식이 중요하다. `@front-react/hooks-and-events`를 직접 import한 뒤, `useDebouncedValue`, load-more window, metrics effect를 하나의 앱 흐름으로 묶는다. 그래서 문서도 `series map + 본문 1편`이 가장 적절했다.

## 이번 재작성의 근거

- `react-internals/04-runtime-demo-app/problem/README.md`
- `react-internals/04-runtime-demo-app/docs/README.md`
- `react-internals/04-runtime-demo-app/docs/references/verification-notes.md`
- `react-internals/04-runtime-demo-app/ts/README.md`
- `react-internals/04-runtime-demo-app/ts/src/app.ts`
- `react-internals/04-runtime-demo-app/ts/src/data.ts`
- `react-internals/04-runtime-demo-app/ts/tests/demo.test.ts`
- `react-internals/04-runtime-demo-app/package.json`

## 현재 검증 상태

```bash
npm run verify --workspace @front-react/runtime-demo-app
```

- 2026-03-14 재실행 기준 `vitest` 3개 테스트 통과
- `tsc --noEmit` typecheck 통과
- verify 전체 통과

## 본문

- [10-making-the-runtime-survive-a-real-app.md](10-making-the-runtime-survive-a-real-app.md)
  - shared runtime 소비, debounce/effect 상호작용, load-more window, metrics 관찰값을 순서대로 따라간다.

## 이번에 명시적으로 남긴 경계

- runtime 코드를 복사하지 않고 패키지 dependency로 소비한다.
- 이 소비는 published package install 검증이라기보다 monorepo workspace dependency `*`를 통한 package-boundary 확인에 가깝다.
- metrics는 profiler가 아니라 학습용 관찰값이다.
- 특히 `renderCount`는 모든 commit의 절대 개수를 세는 계측기라기보다 query/window 변화 effect가 남긴 샘플에 가깝다.
- 실제 네트워크 계층, persistence, infinite scroll observer는 아직 없다.
