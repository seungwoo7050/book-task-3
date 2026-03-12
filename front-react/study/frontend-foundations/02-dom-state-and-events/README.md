# 02 DOM State And Events

상태: `verified`

## 무슨 문제인가

filter, sort, selection, inline edit, URL query state, local persistence를 한 화면에 올리면 상태를 어디에 저장하고 어떤 이벤트로 다시 그릴지가 금방 복잡해진다. 이 프로젝트는 task/workspace board를 예제로 삼아 브라우저 state 동기화 문제를 직접 푼다.

## 왜 필요한가

프레임워크 state 관리 이전에 브라우저 상태와 상호작용이 실제로 어떻게 이어지는지 이해해야 한다. 이 단계는 "이벤트가 발생했을 때 어떤 상태를 어디에 저장하고 어떻게 다시 그릴 것인가"를 직접 설명할 수 있게 만든다.

## 내가 만든 답

search, status filter, sort, row selection, inline edit, URL serialization, localStorage persistence를 함께 묶은 board UI를 `vanilla/`로 구현했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [vanilla/README.md](vanilla/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `vanilla/src/state.ts`에서 query parsing, serialization, persistence helper를 분리한다.
- `vanilla/src/app.ts`에서 root-level `input`, `click`, `keydown` delegation으로 UI를 갱신한다.
- rerender 뒤에도 검색과 selection 흐름이 끊기지 않도록 focus 복원을 명시적으로 처리한다.

## 검증

```bash
cd study
npm run dev --workspace @front-react/dom-state-and-events
npm run verify --workspace @front-react/dom-state-and-events
```

- 검증 기준일: 2026-03-08
- `vitest`: state helper와 query serialization을 포함해 `6`개 테스트 통과
- `playwright`: query -> select -> edit -> save 핵심 흐름 `2`개 시나리오 통과

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [vanilla/README.md](vanilla/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- 실제 network request와 server cache는 아직 없다.
- multi-select, drag and drop, schema migration은 범위 밖이다.
- 다음 단계인 `03-networked-ui-patterns`에서 비동기 요청 상태와 request race를 다룬다.
