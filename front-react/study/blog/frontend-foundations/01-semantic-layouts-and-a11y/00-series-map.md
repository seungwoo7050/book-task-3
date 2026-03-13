# 01 Semantic Layouts And A11y

semantic landmark, labeled form, keyboard validation flow를 vanilla DOM으로 처음부터 짠 프로젝트다. 겉으로는 작은 설정 화면이지만, 실제 주제는 "상태를 붙이기 전에 화면이 먼저 읽히도록 만들 수 있는가"에 가깝다.

## 왜 이 순서로 읽는가

이 프로젝트는 구현 축이 하나로 또렷하다. semantic shell을 먼저 고정하고, 그 위에 validation 규칙을 얹고, 마지막에 브라우저에서 keyboard path를 증명한다. 그래서 글도 한 편이면 충분하다.

## 근거로 사용한 자료

- `frontend-foundations/01-semantic-layouts-and-a11y/README.md`
- `frontend-foundations/01-semantic-layouts-and-a11y/docs/README.md`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/validation.ts`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/shell.test.ts`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/semantic-layout.spec.ts`

## 현재 검증 상태

- `npm run verify --workspace @front-react/semantic-layouts-a11y`
- 2026-03-13 replay 기준 `vitest` 5개, `playwright` 2개 시나리오 통과

## 본문

- [10-semantic-shell-before-state.md](10-semantic-shell-before-state.md)
  - 왜 semantic shell을 먼저 못 박아야 뒤 단계의 상태 로직이 단순해졌는지 따라간다.
