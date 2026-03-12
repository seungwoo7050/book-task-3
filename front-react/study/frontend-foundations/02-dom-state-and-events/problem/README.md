# 문제 정의

프로비넌스: `authored`

## 문제

task/workspace board에서 selection, filter, sort, inline edit, URL query state, local persistence를 동시에 다루면 이벤트 처리와 상태 저장 위치가 복잡해진다. 이 프로젝트는 브라우저 state를 어디에 두고 어떻게 다시 그릴지 설명 가능한 형태로 구현한다.

## 제공 자산

- 이 문서: 문제 정의와 범위
- `data/`: 별도 fixture가 필요 없는 단계를 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder

## 제약

- React 없이 vanilla DOM에서 상태와 이벤트를 직접 관리한다.
- query state와 local UI state의 경계를 분리해야 한다.
- rerender 뒤에도 핵심 keyboard 흐름이 유지되어야 한다.

## 포함 범위

- filter and sort controls
- row selection and inline edit
- localStorage persistence
- URL query sync
- keyboard interaction

## 제외 범위

- 실제 network request
- complex authentication
- server cache

## 요구 산출물

- `vanilla/`에 실행 가능한 board 구현
- query serialization, persistence, selection 규칙을 설명하는 공개 문서
- state helper와 핵심 keyboard 흐름을 검증하는 테스트

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/dom-state-and-events
```

- `vitest`: state helper, query serialization, persistence 로직 확인
- `playwright`: query -> select -> edit -> save 흐름 확인
