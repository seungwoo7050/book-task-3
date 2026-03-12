# Deep Link State Mapping

Deep link는 단순히 화면 이름 하나를 여는 작업이 아니다.
중첩 navigator를 쓰면 URL이 root stack, drawer, tabs, inner stack 상태를 모두 복원해야 한다.

## Mapping Shape

`myapp://detail/abc123`

1. root stack: `Drawer`
2. drawer screen: `Main`
3. tab screen: `HomeTab`
4. inner stack screen: `Detail`
5. route params: `{ id: "abc123", title: "Detail route for abc123" }`

## In This Pilot

- `resolveNavigationState()`가 path를 state로 바꾼다
- `detail/:id`는 title을 URL에 넣지 않고 state hydration으로 보완한다
- unknown path는 `NotFound` fallback으로 내려간다
