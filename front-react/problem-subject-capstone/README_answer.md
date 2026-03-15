# front-react 종합 과제 답안지

이 답안지는 `front-react` capstone의 해법을 실제 코드와 테스트 기준으로 정리한 문서다. 실시간 협업 UI에서 중요한 optimistic update, reconnect replay, presence, conflict surface가 어디서 구현되는지 한 번에 볼 수 있게 구성했다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [03-realtime-collab-workspace](03-realtime-collab-workspace_answer.md) | 시작 위치의 구현을 완성해 외부 backend 없이 완결된 데모여야 한다, 브라우저 탭 두 개만으로 협업 시나리오를 재현할 수 있어야 한다, disconnect/reconnect, queued replay, 충돌 노출이 테스트 가능해야 한다를 한 흐름으로 설명하고 검증한다. 핵심은 metadata와 relativeTime, WorkspaceShell 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd study && npm run verify --workspace @front-react/realtime-collab-workspace` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
