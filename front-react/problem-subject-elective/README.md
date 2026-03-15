# front-react 비필수 문제지

여기서 `비필수`는 중요하지 않다는 뜻이 아니라, 핵심 경로 다음에 읽는 확장 문제라는 뜻입니다. 종합 과제는 sibling `../problem-subject-capstone`에서 다룹니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-ops-triage-console](01-ops-triage-console.md) | 시작 위치의 구현을 완성해 실제 인증, 실제 DB, 실제 백엔드 API 없이 완결된 데모여야 한다, 단일 운영자 시나리오를 기준으로 한다, 실패 시 retry와 undo가 가능해야 하며, keyboard-only 주요 흐름도 지원해야 한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/ops-triage-console` |
| [01-vdom-foundations](01-vdom-foundations.md) | 시작 위치의 구현을 완성해 props.children은 항상 배열이어야 한다, primitive child는 TEXT_ELEMENT로 감싸야 한다, DOM property와 event listener 반영은 updateDom 규칙으로 통일한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run test:vdom && npm run typecheck:vdom && npm run verify:vdom` |
| [02-client-onboarding-portal](02-client-onboarding-portal.md) | 시작 위치의 구현을 완성해 실제 auth backend, server database, email delivery 없이 완결된 데모여야 한다, route guard와 validation 실패 상태가 화면 흐름으로 드러나야 한다, draft restore와 submit retry가 검증 가능한 시나리오여야 한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/client-onboarding-portal` |
| [02-render-pipeline](02-render-pipeline.md) | 시작 위치의 구현을 완성해 @front-react/vdom-foundations의 VNode 구조를 그대로 사용한다, render phase 동안 DOM mutation을 하면 안 된다, keyed/unkeyed child diff를 모두 설명할 수 있어야 한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/render-pipeline` |
| [03-hooks-and-events](03-hooks-and-events.md) | 시작 위치의 구현을 완성해 @front-react/render-pipeline의 diff/patch helper를 그대로 소비한다, hook order invariant를 지켜야 한다, delegated event는 runtime tree 메타데이터를 통해 처리해야 한다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/hooks-and-events` |
| [04-runtime-demo-app](04-runtime-demo-app.md) | 시작 위치의 구현을 완성해 runtime 코드를 복사하지 않고 @front-react/hooks-and-events를 직접 소비해야 한다, debounced search와 pagination이 같은 UI에서 함께 동작해야 한다, metrics는 학습용 관찰값으로만 다루고 production profiler처럼 주장하지 않는다를 한 흐름으로 설명하고 검증한다. | `cd study && npm run verify --workspace @front-react/runtime-demo-app` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
