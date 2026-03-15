# front-react 핵심 답안지

이 답안지는 `front-react`의 핵심 3과제를 실제 소스와 테스트만으로 읽어낼 수 있게 정리한 문서다. leaf 답안지가 없는 세트이므로, 이 문서 자체가 각 과제의 해법과 검증 기준을 함께 제공한다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-semantic-layouts-and-a11y-vanilla](01-semantic-layouts-and-a11y-vanilla_answer.md) | 시작 위치의 구현을 완성해 React 없이 vanilla DOM과 CSS만 사용한다, 정적이지만 상호작용 가능한 UI shell이어야 한다, semantic markup과 keyboard reachability가 DOM 구조만 봐도 드러나야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 FIELD_IDS와 getFieldErrorId, getFieldInput 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/semantic-layouts-a11y` |
| [02-dom-state-and-events-vanilla](02-dom-state-and-events-vanilla_answer.md) | 시작 위치의 구현을 완성해 React 없이 vanilla DOM에서 상태와 이벤트를 직접 관리한다, query state와 local UI state의 경계를 분리해야 한다, rerender 뒤에도 핵심 keyboard 흐름이 유지되어야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 syncUrl와 getSelectedItem, getMarkup 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/dom-state-and-events` |
| [03-networked-ui-patterns-vanilla](03-networked-ui-patterns-vanilla_answer.md) | 시작 위치의 구현을 완성해 실제 서버 대신 mock API를 사용한다, request race와 abort를 무시하지 않고 명시적으로 처리해야 한다, URL query parameter만으로 탐색 상태를 복원할 수 있어야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 buildUrlState와 syncUrl, getMarkup 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/networked-ui-patterns` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
