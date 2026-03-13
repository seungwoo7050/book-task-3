# 01 Semantic Layouts And A11y structure

## opening frame

- 한 줄 훅: semantic shell은 나중에 ARIA를 덧칠하는 일이 아니라 첫 DOM 구조에서 landmark, label, error, focus order를 같이 고정하는 일이다.
- chronology 주의: `46051f3`에 코드와 테스트가 압축돼 있어서, 글은 `problem surface -> validation/focus loop -> verify` 순서로 재구성한다.
- 첫 질문: 설정형 화면에서 "읽히는 구조"와 "탐색 가능한 상호작용"을 vanilla DOM만으로 어떻게 동시에 만들었는가.

## chapter flow

1. README와 `package.json`으로 이 프로젝트가 무엇을 검증하는지 먼저 고정한다.
2. `updateErrorState`와 `mountSettingsShell`을 중심으로 semantic 마크업과 validation/focus loop를 읽는다.
3. unit test와 Playwright smoke를 연결해 public contract를 닫고 남은 경계를 적는다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log --reverse --stat`
- 본문 1: `vanilla/src/app.ts`의 `getAppMarkup`
- 본문 2: `vanilla/src/app.ts`의 `updateErrorState`/`mountSettingsShell`, `vanilla/src/validation.ts`
- 본문 3: `npm run verify --workspace @front-react/semantic-layouts-a11y` 출력과 `vanilla/tests/semantic-layout.spec.ts`

## tone guardrails

- 접근성을 checklist 요약으로 쓰지 않고, 왜 이 구조가 validation/focus 판단의 전환점인지 설명한다.
- 기존 notion과 새 blog 파일은 입력에서 제외한다.
- 코드 스니펫은 짧게 유지하되, `aria-invalid`, inline error, focus 이동이 왜 같이 있어야 하는지 길게 풀어쓴다.
