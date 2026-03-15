# front-react 비필수 답안지

이 답안지는 React internals 4개와 portfolio 확장 과제 2개의 해법을 실제 소스와 테스트 기준으로 정리한 문서다. leaf 답안지가 없는 세트라서, 각 항목의 구현 전략과 검증 포인트를 여기서 바로 설명한다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-ops-triage-console](01-ops-triage-console_answer.md) | 시작 위치의 구현을 완성해 실제 인증, 실제 DB, 실제 백엔드 API 없이 완결된 데모여야 한다, 단일 운영자 시나리오를 기준으로 한다, 실패 시 retry와 undo가 가능해야 하며, keyboard-only 주요 흐름도 지원해야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 sections와 metadata, arraysEqual 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/ops-triage-console` |
| [01-vdom-foundations](01-vdom-foundations_answer.md) | 시작 위치의 구현을 완성해 props.children은 항상 배열이어야 한다, primitive child는 TEXT_ELEMENT로 감싸야 한다, DOM property와 event listener 반영은 updateDom 규칙으로 통일한다를 한 흐름으로 설명하고 검증한다. 핵심은 isEvent와 isProperty, isNew 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run test:vdom && npm run typecheck:vdom && npm run verify:vdom` |
| [02-client-onboarding-portal](02-client-onboarding-portal_answer.md) | 시작 위치의 구현을 완성해 실제 auth backend, server database, email delivery 없이 완결된 데모여야 한다, route guard와 validation 실패 상태가 화면 흐름으로 드러나야 한다, draft restore와 submit retry가 검증 가능한 시나리오여야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 sections와 metadata, stepTitles 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/client-onboarding-portal` |
| [02-render-pipeline](02-render-pipeline_answer.md) | 시작 위치의 구현을 완성해 @front-react/vdom-foundations의 VNode 구조를 그대로 사용한다, render phase 동안 DOM mutation을 하면 안 된다, keyed/unkeyed child diff를 모두 설명할 수 있어야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 diffProps와 isEmptyPropsPatch, diffChildrenByIndex 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/render-pipeline` |
| [03-hooks-and-events](03-hooks-and-events_answer.md) | 시작 위치의 구현을 완성해 @front-react/render-pipeline의 diff/patch helper를 그대로 소비한다, hook order invariant를 지켜야 한다, delegated event는 runtime tree 메타데이터를 통해 처리해야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 currentRoot와 currentHookContext, normalizeChild 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/hooks-and-events` |
| [04-runtime-demo-app](04-runtime-demo-app_answer.md) | 시작 위치의 구현을 완성해 runtime 코드를 복사하지 않고 @front-react/hooks-and-events를 직접 소비해야 한다, debounced search와 pagination이 같은 UI에서 함께 동작해야 한다, metrics는 학습용 관찰값으로만 다루고 production profiler처럼 주장하지 않는다를 한 흐름으로 설명하고 검증한다. 핵심은 PAGE_SIZE와 DEBOUNCE_MS, useDebouncedValue 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/runtime-demo-app` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
