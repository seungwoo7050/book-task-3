# 03 Hooks And Events structure

## opening frame

- 한 줄 훅: 이 단계는 hooks를 추가한 것이 아니라, state 변화와 effect cleanup, event bubbling이 같은 runtime 위에서 굴러가게 만든 단계다.
- chronology 주의: 핵심 구현이 `runtime.ts` 한 파일에 압축돼 있으므로, 글은 `runtime metadata -> hook slot/effect timing -> verify` 순서로 세운다.
- 첫 질문: function component state, effect cleanup, delegated event를 어떤 invariant로 하나의 runtime에 붙였는가.

## chapter flow

1. README와 problem 문서로 runtime integration 문제임을 먼저 고정한다.
2. `dispatchDelegatedEvent`와 `syncEventListeners`로 event metadata 흐름을 설명한다.
3. `useState`/`useEffect`와 verify 결과로 hook slot/effect timing contract를 닫는다.

## evidence allocation

- 도입: `README.md`, `problem/README.md`, `git log`
- 본문 1: `ts/src/runtime.ts`의 delegated event 관련 블록
- 본문 2: `ts/src/runtime.ts`의 `useState`, `useEffect`
- 본문 3: `npm run verify --workspace @front-react/hooks-and-events`와 `ts/tests/*`

## tone guardrails

- hooks API 사용법으로 흐르지 말고, 왜 slot index와 cleanup timing이 runtime invariant인지 설명한다.
- state/effect/event를 따로 요약하지 않고 같은 render loop로 묶어 서술한다.
- notion과 새 blog는 입력 근거에서 제외한다.
