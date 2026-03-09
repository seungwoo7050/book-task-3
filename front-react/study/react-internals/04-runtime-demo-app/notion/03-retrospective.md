# 회고 — demo app을 만들면서 배운 것

## internals 트랙 전체를 관통하는 회고

이 프로젝트는 react-internals 트랙의 마지막이다. 네 프로젝트를 순서대로 만들면서 하나의 의존 체인이 완성됐다:

```
vdom-foundations → render-pipeline → hooks-and-events → runtime-demo-app
```

각 프로젝트가 이전 프로젝트를 npm workspace 의존으로 참조하고, 자기 역할만 추가한다. 이 구조가 "학습을 위한 모듈 분해"가 아니라 "실제로 작동하는 패키지 계층"이라는 것을 demo app이 증명한다.

## "소비자" 관점에서 보는 runtime

이전 세 프로젝트에서는 runtime을 만드는 쪽이었다. 이번에는 쓰는 쪽이다.

소비자 입장에서 runtime API는 놀랍도록 작다: createElement, render, useState, useEffect — 네 개면 앱을 만들 수 있다. 이 네 함수 뒤에 VNode 생성, diff/patch, fiber reconciliation, hook slot, effect lifecycle, delegated event가 전부 숨어 있다.

이 경험이 React를 쓸 때도 적용된다. "React의 API는 왜 이렇게 작은가?"에 대한 답이 여기에 있다 — 복잡성이 없어서가 아니라, 잘 숨겨져 있기 때문이다.

## 커스텀 hook이 작동한다는 것의 의미

useDebouncedValue는 React 프로젝트에서 흔히 쓰는 패턴이다. 이 패턴이 직접 만든 runtime에서도 작동한다는 건, hook slot model이 "호출 순서 기반 인덱싱"이라는 가정 위에서 충분히 범용적이라는 뜻이다.

커스텀 hook 안에서 useState와 useEffect를 호출하면, HookContext의 hookIndex가 순서대로 증가하면서 slot array에 접근한다. DemoApp이 useDebouncedValue를 호출하면, DemoApp의 slot array에 useDebouncedValue 내부의 state slot과 effect slot이 순서대로 자리잡는다.

이것이 "hook은 단순히 함수 호출이다"라는 React 문서의 문장이 코드로 확인되는 순간이다.

## 상태 간의 연쇄 반응

DemoApp에서 가장 복잡한 부분은 상태 간의 연쇄다:

```
query → debouncedQuery → filteredItems → visibleItems
                        → visibleCount 리셋
                        → metrics 갱신
```

이 연쇄가 effect를 통해 일어난다. 하나의 input 이벤트가 최종적으로 3~4번의 재렌더를 trigger할 수 있다:
1. query 변경 → 즉시 렌더
2. debounce 타이머 만료 → debouncedQuery 변경 → 렌더
3. visibleCount 리셋 effect → 렌더
4. metrics 갱신 effect → 렌더

performRender의 `while(root.needsRender)` 루프가 이 연쇄를 한 번의 호출 안에서 처리한다. 루프가 없으면 state update마다 별도의 render가 예약되어 타이밍 문제가 생긴다.

## metrics panel의 솔직함

metrics를 app state로 관리하는 방식은 production으로 가져가기엔 부정확하다. render 시작부터 effect 실행까지의 시간을 재는 건, render phase + commit phase + post-commit effect를 합산하는 것이다. React DevTools처럼 각 phase를 분리해서 재려면 runtime에 profiler hook이 필요하다.

하지만 이 제한을 숨기지 않는 것이 중요하다. docs/concepts/runtime-limitation-note.md에 "이 metrics는 학습용 관찰값이다"라고 명시했고, UI에서도 "Metrics here are learning aids. They show when this runtime redraws more work, not production-grade profiling."이라는 문구를 넣었다.

"한계를 문서화하는 것도 엔지니어링의 일부"라는 걸 배웠다.

## Vite dev server의 역할

이전 프로젝트들은 Vitest + jsdom만으로 검증했다. 이 프로젝트에서 처음으로 Vite dev server를 통해 브라우저에서 실제 동작을 확인한다.

```bash
npm run dev --workspace @front-react/runtime-demo-app
```

이 명령으로 브라우저에서 debounce가 실제로 250ms 후에 작동하는지, CSS가 적용되는지, 반응형 레이아웃이 동작하는지 확인할 수 있다. jsdom은 시각적 검증을 할 수 없으므로, 이 단계에서 dev server가 필수다.

## presentation.md의 존재

이 프로젝트에만 docs/presentation.md가 있다. 5분 발표 흐름이 정리되어 있다. capstone이므로 "보여 주는" 단계가 있고, 그 발표의 핵심 메시지는:

> "이 앱의 포인트는 UI polish가 아니라 shared runtime을 실제 consumer 구조로 끝까지 연결했다는 데 있다."

이 문장이 internals 트랙 전체의 결론이기도 하다.
