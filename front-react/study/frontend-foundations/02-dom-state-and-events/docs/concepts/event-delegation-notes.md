# Event Delegation Notes

row action은 개별 listener를 붙이지 않고 root container에서 처리한다. 이 결정의 목적은 성능 과시가 아니라 구조 단순화다.

핵심 효과는 세 가지다.

- rerender로 row DOM이 바뀌어도 같은 이벤트 경로를 유지할 수 있다.
- `select`, `edit`, `save`, `cancel` 같은 행위가 `data-action`으로 명시돼 테스트가 쉬워진다.
- state transition이 handler별로 흩어지지 않고 `app.ts` 안에서 한눈에 보인다.

이 단계에서는 custom keyboard roving보다 native button interaction을 활용한다. foundations 트랙의 목적이 DOM basics를 명확히 보이는 것이기 때문이다.
