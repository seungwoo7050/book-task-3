# front-react 핵심 문제지

여기서 `essential`은 서버 공통 필수라는 뜻이 아니라, 프론트엔드 학습에서 가장 먼저 읽어야 하는 핵심 경로라는 뜻입니다. 종합 과제는 sibling `../problem-subject-capstone`에서 다룹니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-semantic-layouts-and-a11y-vanilla](01-semantic-layouts-and-a11y-vanilla.md) | 시작 위치의 구현을 완성해 React 없이 vanilla DOM과 CSS만 사용한다, 정적이지만 상호작용 가능한 UI shell이어야 한다, semantic markup과 keyboard reachability가 DOM 구조만 봐도 드러나야 한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/semantic-layouts-a11y` |
| [02-dom-state-and-events-vanilla](02-dom-state-and-events-vanilla.md) | 시작 위치의 구현을 완성해 React 없이 vanilla DOM에서 상태와 이벤트를 직접 관리한다, query state와 local UI state의 경계를 분리해야 한다, rerender 뒤에도 핵심 keyboard 흐름이 유지되어야 한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/dom-state-and-events` |
| [03-networked-ui-patterns-vanilla](03-networked-ui-patterns-vanilla.md) | 시작 위치의 구현을 완성해 실제 서버 대신 mock API를 사용한다, request race와 abort를 무시하지 않고 명시적으로 처리해야 한다, URL query parameter만으로 탐색 상태를 복원할 수 있어야 한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/networked-ui-patterns` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
