# 01 Semantic Layouts And A11y

이 프로젝트의 핵심은 "예쁜 설정 화면"이 아니라, 상태를 거의 붙이지 않은 단계에서도 화면이 먼저 읽히고 탐색될 수 있는가를 검증하는 데 있다. 이번 Todo에서는 semantic landmark, help/error pairing, keyboard-only validation flow, responsive column collapse가 실제 코드와 테스트에서 어떻게 연결되는지 다시 묶었다.

## 왜 이 순서로 읽는가

구현 축이 하나로 선명하다. `getAppMarkup()`로 읽히는 구조를 먼저 고정하고, `validateSettings()`를 순수 함수로 분리한 뒤, 마지막에 Vitest와 Playwright로 keyboard path와 viewport 변화를 재생한다. 그래서 문서도 `series map + 본문 1편`이면 충분했다.

## 이번 재작성의 근거

- `frontend-foundations/01-semantic-layouts-and-a11y/problem/README.md`
- `frontend-foundations/01-semantic-layouts-and-a11y/docs/README.md`
- `frontend-foundations/01-semantic-layouts-and-a11y/docs/references/verification-notes.md`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/README.md`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/app.ts`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/validation.ts`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/src/styles.css`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/shell.test.ts`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/validation.test.ts`
- `frontend-foundations/01-semantic-layouts-and-a11y/vanilla/tests/semantic-layout.spec.ts`

## 현재 검증 상태

```bash
npm run build --workspace @front-react/semantic-layouts-a11y
npm run test --workspace @front-react/semantic-layouts-a11y
npm run e2e --workspace @front-react/semantic-layouts-a11y
```

- 2026-03-14 재실행 기준 `vite build` 통과
- `vitest` 5개 테스트 통과
- `playwright` 2개 시나리오 통과

## 본문

- [10-semantic-shell-before-state.md](10-semantic-shell-before-state.md)
  - semantic shell을 먼저 못 박은 뒤 validation과 keyboard flow를 그 구조에 투영하는 과정을 따라간다.

## 이번에 명시적으로 남긴 경계

- 접근성 자동화는 landmark, label, keyboard flow까지는 확인하지만 실제 스크린리더 읽기 순서를 완전히 대체하지는 않는다.
- responsive 검증은 `gridTemplateColumns` 기준으로 column collapse를 확인한다.
- persistence, routing, network state는 아직 범위 밖이다.
